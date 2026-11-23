#!/usr/bin/env python3
"""
Verify the GA4 connection and list every property this account can read.
Use the printed property IDs in the advertiser report config.
Run: python3 scripts/ga-test.py
"""

import json
import os
import urllib.error
import urllib.request

import google.auth.transport.requests
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "secrets", "ga-credentials.json")
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

if not os.path.exists(CREDENTIALS_FILE):
    raise SystemExit("No GA credentials found. Run: python3 scripts/ga-auth.py")

with open(CREDENTIALS_FILE) as f:
    data = json.load(f)

creds = Credentials(
    token=None,
    refresh_token=data["refresh_token"],
    client_id=data["client_id"],
    client_secret=data["client_secret"],
    token_uri=data["token_uri"],
    scopes=SCOPES,
)

creds.refresh(google.auth.transport.requests.Request())


def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {creds.token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise SystemExit(f"\nHTTP {e.code} from {url}\n{body}\n")


summaries = get("https://analyticsadmin.googleapis.com/v1beta/accountSummaries?pageSize=200")

accounts = summaries.get("accountSummaries", [])
if not accounts:
    raise SystemExit(
        "Connected, but this Google account can read no GA4 properties.\n"
        "Grant it at least Viewer on the MRF and directory properties."
    )

print("Connection successful.\n")
for acct in accounts:
    print(f"{acct.get('displayName')}  ({acct.get('account')})")
    for prop in acct.get("propertySummaries", []):
        prop_id = prop.get("property", "").split("/")[-1]
        print(f"    {prop_id:<14} {prop.get('displayName')}")
    print()
