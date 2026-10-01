#!/usr/bin/env python3
"""Run GAM performance report for Enverus and save data."""

import json, os, time, urllib.request, urllib.parse, urllib.error
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "secrets", "gam-credentials.json")
NETWORK_CODE = "6933594"
ORDER_NAME = "MRF Enverus 2026/06"
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
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print("Error:", e.read().decode())
        raise

print("Creating report...")
report = post("reports", {
    "displayName": "Enverus All-Time Performance",
    "reportDefinition": {
        "reportType": "HISTORICAL",
        "dimensions": ["DATE", "ORDER_NAME", "LINE_ITEM_NAME", "AD_UNIT_NAME"],
        "metrics": [
            "AD_SERVER_IMPRESSIONS",
            "AD_SERVER_CLICKS",
            "AD_SERVER_CTR",
        ],
        "dateRange": {
            "fixed": {
                "startDate": {"year": 2026, "month": 6, "day": 1},
                "endDate": {"year": 2026, "month": 6, "day": 30},
            }
        },
    },
})
report_name = report["name"]
report_id = report["reportId"]
print(f"Report: {report_name}")

print("Running report...")
run_op = post(f"reports/{report_id}:run", {})
op_name = run_op.get("name", "")
print(f"Operation: {op_name}")

# Poll
op_short = op_name.replace(f"networks/{NETWORK_CODE}/", "")
for i in range(30):
    time.sleep(3)
    op = get(op_short)
    done = op.get("done", False)
    print(f"  Poll {i+1}: done={done}")
    if done:
        break

if not op.get("done"):
    print("Timed out.")
    exit(1)

if "error" in op:
    print("Report error:", json.dumps(op["error"], indent=2))
    exit(1)

print("Fetching rows...")
rows_resp = post(f"reports/{report_id}:fetchRows", {})
print(json.dumps(rows_resp, indent=2)[:2000])

out = {"report": report, "operation": op, "rows": rows_resp}
out_file = os.path.join(os.path.dirname(__file__), "..", "secrets", "enverus-report-raw.json")
with open(out_file, "w") as f:
    json.dump(out, f, indent=2)
print(f"\nSaved to {out_file}")
