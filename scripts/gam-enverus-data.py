#!/usr/bin/env python3
"""Pull Enverus data and run a performance report."""

import json, os, time, urllib.request, urllib.parse, urllib.error
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "secrets", "gam-credentials.json")
NETWORK_CODE = "6933594"
ORDER_RESOURCE = f"networks/{NETWORK_CODE}/orders/4098403169"
BASE = f"https://admanager.googleapis.com/v1/networks/{NETWORK_CODE}"

with open(CREDENTIALS_FILE) as f:
    data = json.load(f)

creds = Credentials(
    token=None,
    refresh_token=data["refresh_token"],
    client_id=data["client_id"],
    client_secret=data["client_secret"],
    token_uri=data["token_uri"],
    scopes=["https://www.googleapis.com/auth/admanager"],
)
creds.refresh(google.auth.transport.requests.Request())

def get(path, params=None):
    url = f"{BASE}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {creds.token}"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def post(path, body):
    url = f"{BASE}/{path}"
    payload = json.dumps(body).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# Line items
print("=== Line Items ===")
line_items = get("lineItems", {"filter": f'order="{ORDER_RESOURCE}"'})
print(json.dumps(line_items, indent=2))

# Create report
print("\n=== Creating Report ===")
report = post("reports", {
    "displayName": "Enverus All-Time Performance",
    "reportDefinition": {
        "dimensions": ["DATE", "LINE_ITEM_NAME"],
        "metrics": [
            "TOTAL_LINE_ITEM_LEVEL_IMPRESSIONS",
            "TOTAL_LINE_ITEM_LEVEL_CLICKS",
            "TOTAL_LINE_ITEM_LEVEL_CTR",
        ],
        "dateRange": {
            "startDate": {"year": 2026, "month": 6, "day": 1},
            "endDate": {"year": 2026, "month": 12, "day": 31},
        },
        "dimensionFilters": [{
            "fieldName": "ORDER_ID",
            "values": ["4098403169"],
        }],
    },
})
print("Report created:", report.get("name"))

# Run the report
report_name = report["name"]
run_result = post(f"{report_name.replace(f'networks/{NETWORK_CODE}/', '')}/run", {})
print("Run result:", json.dumps(run_result, indent=2))
