#!/usr/bin/env python3
"""Explore GAM data for Enverus advertiser."""

import json
import os
import urllib.request
import urllib.parse
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "secrets", "gam-credentials.json")
NETWORK_CODE = "6933594"
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

# Find Enverus company
print("=== Companies matching 'Enverus' ===")
result = get("companies", {"filter": "displayName:Enverus"})
print(json.dumps(result, indent=2))

# Find orders for Enverus
print("\n=== Orders matching 'Enverus' ===")
result = get("orders", {"filter": "displayName:Enverus"})
print(json.dumps(result, indent=2))
