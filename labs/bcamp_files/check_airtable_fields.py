"""
check_airtable_fields.py
────────────────────────
Scans every field name in every table of an Airtable base for hidden /
non-printable special characters that are silently introduced when tables
are created from CSV files.

Characters detected
───────────────────
  \ufeff  BOM (byte-order mark)               – very common in CSV exports
  \u00a0  Non-breaking space
  \u200b  Zero-width space
  \u200c  Zero-width non-joiner
  \u200d  Zero-width joiner
  \u00ad  Soft hyphen
  \u200e  Left-to-right mark
  \u200f  Right-to-left mark
  \u2060  Word joiner
  \ufffe  Reversed BOM
  \x00-\x1f / \x7f-\x9f  ASCII / Latin-1 control characters
  Leading / trailing whitespace (spaces, tabs, newlines)

Usage
─────
1. Install dependency:
      pip install requests

2. Set your credentials – either as environment variables:
      export AIRTABLE_TOKEN="patXXXXXXXXXXXXXX"
      export AIRTABLE_BASE_ID="appXXXXXXXXXXXXXX"

   or edit the two constants at the top of the script.

3. Run in CHECK mode (safe, read-only):
      python check_airtable_fields.py

4. Run in FIX mode to automatically rename dirty fields:
      python check_airtable_fields.py --fix

   Requires a personal access token with the `schema:bases:write` scope.

API docs
────────
  Metadata  https://airtable.com/developers/web/api/field-model
  Auth      https://airtable.com/developers/web/guides/personal-access-tokens
"""

import os
import re
import sys
import json
import argparse
import unicodedata
import requests

# ── Credentials ──────────────────────────────────────────────────────────────
AIRTABLE_TOKEN  = os.getenv("AIRTABLE_TOKEN",  "YOUR_PERSONAL_ACCESS_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "YOUR_BASE_ID")

# ── Hidden-character patterns ─────────────────────────────────────────────────
#   Covers: BOM, zero-width chars, soft hyphen, directional marks,
#           ASCII control chars (0x00-0x1F, 0x7F), C1 controls (0x80-0x9F)
HIDDEN_CHAR_RE = re.compile(
    r"[\ufeff\ufffe\u00a0\u00ad"
    r"\u200b-\u200f\u2028\u2029\u2060\u2061-\u2064"
    r"\x00-\x1f\x7f-\x9f]"
)

ANSI_RED    = "\033[91m"
ANSI_GREEN  = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_RESET  = "\033[0m"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _headers():
    return {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type":  "application/json",
    }


def get_tables(base_id: str) -> list[dict]:
    """Return the list of tables (with fields) from the Metadata API."""
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
    resp = requests.get(url, headers=_headers(), timeout=15)
    resp.raise_for_status()
    return resp.json().get("tables", [])


def clean_name(name: str) -> str:
    """
    Return a sanitised version of *name*:
      1. Remove every hidden / non-printable character.
      2. Collapse any run of whitespace to a single space.
      3. Strip leading / trailing whitespace.
    """
    cleaned = HIDDEN_CHAR_RE.sub("", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def describe_hidden(name: str) -> list[str]:
    """Return human-readable descriptions of every offending character."""
    found = []
    for ch in name:
        if HIDDEN_CHAR_RE.match(ch):
            cp = ord(ch)
            try:
                desc = unicodedata.name(ch)
            except ValueError:
                desc = f"CONTROL CHARACTER"
            found.append(f"U+{cp:04X} ({desc})")
    # Also flag leading/trailing whitespace
    if name != name.strip():
        found.append("leading/trailing whitespace")
    return found


def rename_field(base_id: str, table_id: str, field_id: str, new_name: str) -> bool:
    """PATCH the field name via the Metadata API. Returns True on success."""
    url = (
        f"https://api.airtable.com/v0/meta/bases/{base_id}"
        f"/tables/{table_id}/fields/{field_id}"
    )
    payload = {"name": new_name}
    resp = requests.patch(url, headers=_headers(),
                          data=json.dumps(payload), timeout=15)
    return resp.status_code == 200


# ── Main logic ────────────────────────────────────────────────────────────────

def run(fix: bool = False):
    if AIRTABLE_TOKEN == "YOUR_PERSONAL_ACCESS_TOKEN":
        sys.exit(
            "ERROR: Set AIRTABLE_TOKEN (env var) or edit the constant in the script."
        )
    if AIRTABLE_BASE_ID == "YOUR_BASE_ID":
        sys.exit(
            "ERROR: Set AIRTABLE_BASE_ID (env var) or edit the constant in the script."
        )

    print(f"\n{'='*62}")
    print(f"  Airtable field-name checker  |  base: {AIRTABLE_BASE_ID}")
    print(f"  Mode: {'FIX (will rename dirty fields)' if fix else 'CHECK only (read-only)'}")
    print(f"{'='*62}\n")

    tables = get_tables(AIRTABLE_BASE_ID)
    print(f"Found {len(tables)} table(s).\n")

    total_fields  = 0
    dirty_fields  = 0
    fixed_fields  = 0
    failed_fields = 0

    report_lines: list[str] = []

    for table in tables:
        table_name = table["name"]
        table_id   = table["id"]
        fields     = table.get("fields", [])

        table_header = f"  Table: {table_name!r}  ({len(fields)} fields)"
        print(table_header)
        print("  " + "-" * (len(table_header) - 2))

        table_dirty = 0

        for field in fields:
            total_fields += 1
            fname    = field["name"]
            field_id = field["id"]
            issues   = describe_hidden(fname)

            if not issues and fname == fname.strip():
                # Field is clean
                print(f"    {ANSI_GREEN}✓{ANSI_RESET}  {fname!r}")
                continue

            # ── Dirty field ──────────────────────────────────────────────────
            dirty_fields += 1
            table_dirty  += 1
            suggestion   = clean_name(fname)

            print(f"    {ANSI_RED}✗{ANSI_RESET}  {fname!r}")
            for issue in issues:
                print(f"       ↳ {ANSI_YELLOW}{issue}{ANSI_RESET}")
            print(f"       → suggested clean name: {suggestion!r}")

            report_lines.append(
                f"[{table_name}] Field {fname!r} (id={field_id}) "
                f"→ issues: {', '.join(issues)} → clean: {suggestion!r}"
            )

            if fix:
                ok = rename_field(AIRTABLE_BASE_ID, table_id, field_id, suggestion)
                if ok:
                    fixed_fields += 1
                    print(f"       {ANSI_GREEN}✔ Renamed successfully{ANSI_RESET}")
                else:
                    failed_fields += 1
                    print(f"       {ANSI_RED}✘ Rename FAILED – check token scope (schema:bases:write){ANSI_RESET}")

        if table_dirty == 0:
            print(f"    {ANSI_GREEN}All fields look clean.{ANSI_RESET}")
        print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 62)
    print("SUMMARY")
    print("=" * 62)
    print(f"  Tables checked  : {len(tables)}")
    print(f"  Fields checked  : {total_fields}")
    print(f"  Dirty fields    : {dirty_fields}")
    if fix:
        print(f"  Successfully fixed : {fixed_fields}")
        if failed_fields:
            print(f"  {ANSI_RED}Failed renames     : {failed_fields}{ANSI_RESET}")
    print()

    if dirty_fields == 0:
        print(f"{ANSI_GREEN}✔  All field names are clean. Safe to start lab exercises.{ANSI_RESET}\n")
    else:
        if fix:
            if failed_fields == 0:
                print(f"{ANSI_GREEN}✔  All dirty fields have been fixed.{ANSI_RESET}\n")
            else:
                print(f"{ANSI_YELLOW}⚠  Some fields could not be renamed – see above.{ANSI_RESET}\n")
        else:
            print(
                f"{ANSI_YELLOW}⚠  {dirty_fields} dirty field(s) found. "
                f"Re-run with --fix to rename them automatically.{ANSI_RESET}\n"
            )

    # Write a plain-text report alongside the script
    if report_lines:
        report_path = "field_issues_report.txt"
        with open(report_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(report_lines) + "\n")
        print(f"  Detailed report written to: {report_path}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check (and optionally fix) hidden characters in Airtable field names."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically rename dirty fields (requires schema:bases:write scope).",
    )
    args = parser.parse_args()
    run(fix=args.fix)
