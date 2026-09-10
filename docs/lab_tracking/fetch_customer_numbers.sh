#!/usr/bin/env bash
# Run this locally with your own temporary Webex admin personal access token.
# Get one at https://developer.webex.com/docs/getting-started (valid 12 hours).
# This script never sends the token anywhere except api.webex.com, and produces
# a JSON file you commit to the repo — the token itself is never stored anywhere.
#
# Usage:
#   WEBEX_TOKEN="your_temp_admin_token" ./fetch_customer_numbers.sh > customer_profile_numbers.json

set -euo pipefail

if [ -z "${WEBEX_TOKEN:-}" ]; then
  echo "Set WEBEX_TOKEN first, e.g.: WEBEX_TOKEN=xxxx ./fetch_customer_numbers.sh" >&2
  exit 1
fi

echo "{"
for i in $(seq 1 10); do
  email="customer${i}@wxone.wbx.ai"
  number=$(curl -s "https://webexapis.com/v1/people?email=${email}&callingData=true" \
    -H "Authorization: Bearer ${WEBEX_TOKEN}" \
    -H "Accept: application/json" \
    | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
    items = data.get("items", [])
    if not items:
        print("")
        sys.exit()
    phones = items[0].get("phoneNumbers", [])
    match = next((p["value"] for p in phones if p.get("type") == "work" and p.get("primary") is True), "")
    print(match)
except Exception:
    print("")
')
  comma=","
  if [ "$i" -eq 10 ]; then comma=""; fi
  if [ -z "$number" ]; then
    echo "  Could not find a number for ${email} — skipping (check the token/email/org)." >&2
    continue
  fi
  echo "  \"${i}\": \"${number}\"${comma}"
done
echo "}"

