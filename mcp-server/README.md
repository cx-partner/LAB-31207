# LAB-31207 MCP server

This is the isolated MCP backend for the LAB-31207 debt-collection AI Agent.
It exposes these tools:

- `authenticate_user(pin)` — returns two randomly selected PIN positions and their digits.
- `fetch_balance(phone_number)` — finds a customer by normalized phone number and returns account context, including the full PIN and payment-delivery context approved for this lab.
- `payment_session(debt_amount, email, mobile_number, webex_calling)` — creates a NovaPay session and optionally posts its delivery payload to `PAYMENT_DELIVERY_WEBHOOK_URL`.
- `confirm_payment(record_id, payment_session_id)` — confirms a completed NovaPay session and updates the Airtable balance once.
- `fetch_transactions(customer_id)` — returns the five most-recent linked transactions.

## Airtable retry behavior

Every Airtable `GET` makes one additional attempt only when the first response
is an HTTP 5xx status. Airtable writes are never retried.

## Deployment

The service is deployed to `/opt/mcp/LAB-31207` and exposed through:

`https://mcp.cx-tme.com/lab-31207/mcp`

Keep the populated `.env` on the EC2 host only. The service uses a local SQLite
ledger to make `confirm_payment` idempotent across repeated agent calls.

The delivery webhook receives `paymentUrl`, `mobileNumber`, `email`,
`webexCalling`, `amount`, and `sessionId`. It must send the link by SMS when
`webexCalling` is `false`, and by email when it is `true`.

## Airtable requirement

The `Customers` table must have a checkbox field named `WebexCalling`. The
server verifies this schema before returning a customer record. An unchecked
checkbox is treated as `false` (personal US mobile/SMS); a checked box is
`true` (Webex Calling/email). The lab prework page writes this value for newly
provisioned records.
