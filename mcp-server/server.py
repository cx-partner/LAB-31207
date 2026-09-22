"""MCP tools for the LAB-31207 debt-collection AI Agent.

Only Airtable reads receive one retry after a 5xx response. Airtable writes are
performed once because repeating an ambiguous write could duplicate a payment.
"""

from __future__ import annotations

import json
import logging
import os
import re
import secrets
import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.debug import DebugTokenVerifier


load_dotenv()

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
LOGGER = logging.getLogger("lab_31207_mcp")

AIRTABLE_API_URL = "https://api.airtable.com/v0"
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "")
MCP_API_KEY = os.getenv("MCP_API_KEY", "")
NOVAPAY_URL = os.getenv("NOVAPAY_URL", "http://127.0.0.1:8082/api/create-session")
NOVAPAY_STATUS_URL = os.getenv(
    "NOVAPAY_STATUS_URL", "http://127.0.0.1:8082/api/session-status"
)
PAYMENT_DELIVERY_WEBHOOK_URL = os.getenv("PAYMENT_DELIVERY_WEBHOOK_URL", "")
PAYMENT_LEDGER_PATH = Path(
    os.getenv("PAYMENT_LEDGER_PATH", ".data/payment-ledger.sqlite3")
)
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8086"))


class ConfigurationError(RuntimeError):
    """Raised when a required server-side setting is absent."""


def require_airtable_configuration() -> None:
    if not AIRTABLE_BASE_ID or not AIRTABLE_API_KEY:
        raise ConfigurationError("Airtable is not configured on this MCP server.")


def normalize_phone_number(phone_number: str) -> str:
    normalized = re.sub(r"\D", "", phone_number)
    if not normalized:
        raise ValueError("phone_number must contain at least one digit.")
    return normalized


def normalize_pin(pin: str) -> str:
    normalized = pin.strip()
    if not re.fullmatch(r"\d{4}", normalized):
        raise ValueError("pin must contain exactly four digits.")
    return normalized


def webex_calling_value(value: Any) -> bool:
    """Return a strict boolean for an Airtable checkbox value."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, str) and value.strip().lower() in {"true", "false"}:
        return value.strip().lower() == "true"
    raise ValueError("WebexCalling must be a boolean Airtable field.")


@dataclass(frozen=True)
class AirtableClient:
    base_id: str
    api_key: str

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{AIRTABLE_API_URL}/{self.base_id}/{path.lstrip('/')}"

    def _get(self, url: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run a GET with exactly one retry on an HTTP 5xx response."""
        with httpx.Client(timeout=15) as client:
            for attempt in range(2):
                response = client.get(url, headers=self.headers, params=params)
                if 500 <= response.status_code <= 599 and attempt == 0:
                    LOGGER.warning("Airtable GET returned %s; retrying once", response.status_code)
                    continue
                response.raise_for_status()
                return response.json()
        raise RuntimeError("Unreachable Airtable read state.")

    def read(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get(self._url(path), params=params)

    def customer_delivery_field_exists(self) -> bool:
        """Confirm the required Customers checkbox exists before routing payment links."""
        schema = self._get(f"{AIRTABLE_API_URL}/meta/bases/{self.base_id}/tables")
        customers = next(
            (table for table in schema.get("tables", []) if table.get("name") == "Customers"),
            None,
        )
        if customers is None:
            raise ValueError("Customers table is not available in the Airtable base.")
        return any(
            field.get("name") == "WebexCalling" and field.get("type") == "checkbox"
            for field in customers.get("fields", [])
        )

    def patch(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Run one Airtable PATCH. Writes are deliberately never retried."""
        with httpx.Client(timeout=15) as client:
            response = client.patch(self._url(path), headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()


def airtable() -> AirtableClient:
    require_airtable_configuration()
    return AirtableClient(AIRTABLE_BASE_ID, AIRTABLE_API_KEY)


def find_customer_by_phone(phone_number: str) -> dict[str, Any] | None:
    normalized = normalize_phone_number(phone_number)
    response = airtable().read(
        "Customers",
        params={
            "filterByFormula": f"{{PhoneNumber}}='{normalized}'",
            "maxRecords": 1,
        },
    )
    return (response.get("records") or [None])[0]


def find_customer_by_id(customer_id: str) -> dict[str, Any] | None:
    normalized = customer_id.strip()
    if not normalized:
        raise ValueError("customer_id is required.")
    response = airtable().read(
        "Customers",
        params={
            "filterByFormula": f"{{CustomerID}}='{normalized.replace("'", "\\'")}'",
            "maxRecords": 1,
        },
    )
    return (response.get("records") or [None])[0]


class PaymentLedger:
    """Local idempotency ledger for completed NovaPay sessions."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.Lock()

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS payment_confirmations (
                    payment_session_id TEXT PRIMARY KEY,
                    record_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    confirmation_code TEXT,
                    remaining_balance REAL,
                    state TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT
                )
                """
            )

    def get(self, payment_session_id: str) -> dict[str, Any] | None:
        with sqlite3.connect(self.path) as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                "SELECT * FROM payment_confirmations WHERE payment_session_id = ?",
                (payment_session_id,),
            ).fetchone()
        return dict(row) if row else None

    def reserve(self, payment_session_id: str, record_id: str, amount: float) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """
                INSERT INTO payment_confirmations (
                    payment_session_id, record_id, amount, state
                ) VALUES (?, ?, ?, 'applying')
                """,
                (payment_session_id, record_id, amount),
            )

    def complete(
        self,
        payment_session_id: str,
        confirmation_code: str,
        remaining_balance: float,
    ) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """
                UPDATE payment_confirmations
                SET state = 'completed', confirmation_code = ?,
                    remaining_balance = ?, completed_at = CURRENT_TIMESTAMP
                WHERE payment_session_id = ?
                """,
                (confirmation_code, remaining_balance, payment_session_id),
            )


LEDGER = PaymentLedger(PAYMENT_LEDGER_PATH)


def error_response(message: str) -> dict[str, str]:
    LOGGER.warning("Tool request failed: %s", message)
    return {"error": message}


auth_provider = DebugTokenVerifier(validate=lambda token: bool(MCP_API_KEY) and token == MCP_API_KEY)
mcp = FastMCP(
    name="LAB-31207 Debt Collection MCP Server",
    instructions=(
        "Provides secure debt-collection account lookup, PIN challenge, NovaPay "
        "payment confirmation, and recent-transaction tools for Webex AI Agent."
    ),
    auth=auth_provider,
)


@mcp.tool()
def authenticate_user(pin: str) -> dict[str, Any]:
    """Return two random positions and the corresponding digits from a four-digit PIN.

    Call this only after `fetch_balance` returns the customer's PIN. The caller must
    provide the requested digits; the AI Agent validates the caller response.
    """
    try:
        normalized_pin = normalize_pin(pin)
        positions = sorted(secrets.SystemRandom().sample(range(4), 2))
        return {
            "challenge": [
                {"position": position + 1, "expected_digit": normalized_pin[position]}
                for position in positions
            ]
        }
    except ValueError as error:
        return error_response(str(error))


@mcp.tool()
def fetch_balance(phone_number: str) -> dict[str, Any]:
    """Look up a customer by phone number and return debt-payment account context.

    Returns the Airtable record ID, customer ID, PIN, balance, maturity date, and
    delivery context. The server normalizes phone input to digits before lookup.
    """
    try:
        if not airtable().customer_delivery_field_exists():
            return error_response(
                "Customers.WebexCalling checkbox is required before payment delivery can be used."
            )
        customer = find_customer_by_phone(phone_number)
        if customer is None:
            return {"status": "not_found", "message": "No customer matches that phone number."}
        fields = customer.get("fields", {})
        webex_calling = webex_calling_value(fields.get("WebexCalling"))
        return {
            "status": "found",
            "record_id": customer.get("id", ""),
            "customer_id": fields.get("CustomerID", ""),
            "first_name": fields.get("FirstName", ""),
            "last_name": fields.get("LastName", ""),
            "pin": fields.get("PIN", ""),
            "phone_number": fields.get("PhoneNumber", ""),
            "email": fields.get("Email", ""),
            "webex_calling": webex_calling,
            "delivery_channel": "email" if webex_calling else "sms",
            "balance": fields.get("Balance", 0),
            "maturity_date": fields.get("MaturityDate", ""),
        }
    except (ConfigurationError, ValueError, httpx.HTTPError) as error:
        return error_response(str(error))


@mcp.tool()
def payment_session(
    debt_amount: float, email: str, mobile_number: str, webex_calling: bool
) -> dict[str, Any]:
    """Create a NovaPay payment session and send its delivery payload when configured.

    The payment-delivery webhook is optional while the lab integration is pending.
    Its POST body contains paymentUrl, mobileNumber, email, webexCalling, amount,
    and sessionId. The webhook sends SMS only for personal US mobile numbers and
    email only for Webex Calling profiles.
    """
    if debt_amount <= 0:
        return error_response("debt_amount must be greater than zero.")
    if not email.strip():
        return error_response("email is required.")
    try:
        normalized_mobile_number = normalize_phone_number(mobile_number)
    except ValueError as error:
        return error_response(str(error))

    try:
        with httpx.Client(timeout=15) as client:
            response = client.post(NOVAPAY_URL, json={"amount": debt_amount})
            response.raise_for_status()
            novapay = response.json()

            session_id = str(novapay.get("sessionId", ""))
            payment_url = str(novapay.get("paymentUrl", ""))
            if not session_id or not payment_url:
                return error_response("NovaPay did not return a session ID and payment URL.")

            delivery_status = "not_configured"
            if PAYMENT_DELIVERY_WEBHOOK_URL:
                webhook_response = client.post(
                    PAYMENT_DELIVERY_WEBHOOK_URL,
                    json={
                        "email": email,
                        "paymentUrl": payment_url,
                        "mobileNumber": normalized_mobile_number,
                        "webexCalling": webex_calling,
                        "amount": debt_amount,
                        "sessionId": session_id,
                    },
                )
                webhook_response.raise_for_status()
                delivery_status = "sent"

        return {
            "status": "pending_payment",
            "payment_session_id": session_id,
            "payment_url": payment_url,
            "amount": debt_amount,
            "email": email,
            "mobile_number": normalized_mobile_number,
            "delivery_channel": "email" if webex_calling else "sms",
            "delivery_status": delivery_status,
        }
    except httpx.HTTPError as error:
        return error_response(f"Payment session request failed: {error}")


@mcp.tool()
def confirm_payment(record_id: str, payment_session_id: str) -> dict[str, Any]:
    """Confirm a completed NovaPay payment and deduct it from one Airtable balance.

    This tool is idempotent after a successful confirmation. If an Airtable write
    has an ambiguous failure, it returns `requires_reconciliation` rather than risk
    applying the same payment twice.
    """
    if not record_id.strip() or not payment_session_id.strip():
        return error_response("record_id and payment_session_id are required.")

    try:
        with httpx.Client(timeout=15) as client:
            status_response = client.get(
                NOVAPAY_STATUS_URL,
                params={"sessionId": payment_session_id},
            )
            status_response.raise_for_status()
            payment = status_response.json()
    except httpx.HTTPError as error:
        return error_response(f"Payment-status request failed: {error}")

    if payment.get("status") != "completed":
        return {
            "status": "pending_payment",
            "payment_status": payment.get("status", "unknown"),
            "message": "The NovaPay payment has not completed yet.",
        }

    try:
        amount = float(payment.get("amount", 0))
    except (TypeError, ValueError):
        return error_response("NovaPay returned an invalid payment amount.")
    if amount <= 0:
        return error_response("NovaPay returned a non-positive payment amount.")

    with LEDGER.lock:
        existing = LEDGER.get(payment_session_id)
        if existing and existing["state"] == "completed":
            return {
                "status": "success",
                "already_confirmed": True,
                "amount_paid": existing["amount"],
                "confirmation_code": existing["confirmation_code"],
                "remaining_balance": existing["remaining_balance"],
            }
        if existing:
            return {
                "status": "requires_reconciliation",
                "message": "This payment has an unresolved prior balance-update attempt.",
            }

        try:
            customer = airtable().read(f"Customers/{record_id}")
            current_balance = float(customer.get("fields", {}).get("Balance", 0))
            if amount > current_balance:
                return error_response("Payment amount exceeds the current account balance.")

            remaining_balance = round(current_balance - amount, 2)
            LEDGER.reserve(payment_session_id, record_id, amount)
            airtable().patch(
                f"Customers/{record_id}",
                {"fields": {"Balance": remaining_balance}},
            )
            confirmation_code = str(payment.get("confirmationCode", ""))
            LEDGER.complete(payment_session_id, confirmation_code, remaining_balance)
            return {
                "status": "success",
                "amount_paid": amount,
                "confirmation_code": confirmation_code,
                "remaining_balance": remaining_balance,
            }
        except (ConfigurationError, httpx.HTTPError, ValueError) as error:
            return {
                "status": "requires_reconciliation",
                "message": f"Balance update was not retried: {error}",
            }


@mcp.tool()
def fetch_transactions(customer_id: str) -> dict[str, Any]:
    """Return up to five most-recent transactions for a customer account."""
    try:
        customer = find_customer_by_id(customer_id)
        if customer is None:
            return {"status": "not_found", "message": "No customer matches that customer ID."}

        transaction_record_ids = customer.get("fields", {}).get("Transactions", [])
        transactions: list[dict[str, Any]] = []
        for transaction_record_id in transaction_record_ids:
            transaction = airtable().read(f"Transactions/{transaction_record_id}")
            fields = transaction.get("fields", {})
            transactions.append(
                {
                    "record_id": transaction.get("id", ""),
                    "transaction_id": fields.get("TransactionID", ""),
                    "amount": fields.get("Amount", 0),
                    "vendor": fields.get("Vendor", ""),
                    "city": fields.get("City", ""),
                    "date": fields.get("Date", ""),
                }
            )

        transactions.sort(key=lambda transaction: transaction["date"] or "", reverse=True)
        return {
            "status": "found",
            "customer_id": customer.get("fields", {}).get("CustomerID", ""),
            "transactions": transactions[:5],
        }
    except (ConfigurationError, ValueError, httpx.HTTPError) as error:
        return error_response(str(error))


if __name__ == "__main__":
    LEDGER.initialize()
    mcp.run(transport="streamable-http", host=HOST, port=PORT)
