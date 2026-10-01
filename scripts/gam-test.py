#!/usr/bin/env python3
"""Test GAM API connection by fetching network info."""

import json
import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "secrets", "gam-credentials.json")
NETWORK_CODE = "6933594"

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

import urllib.request

url = f"https://admanager.googleapis.com/v1/networks/{NETWORK_CODE}"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {creds.token}"})
with urllib.request.urlopen(req) as resp:
    network = json.loads(resp.read())

print("Connection successful.")
print(f"Network: {network.get('displayName')} ({network.get('name')})")
print(f"Currency: {network.get('currencyCode')}")
print(f"Timezone: {network.get('timeZone')}")
