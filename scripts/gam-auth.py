#!/usr/bin/env python3
"""
One-time OAuth flow to get a GAM API refresh token.
Run: python3 scripts/gam-auth.py
"""

import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET_FILE = os.path.expanduser(
    "~/Downloads/client_secret_896537630194-oc56mk0ucfdqsrg5a3a25bg97hp74hk5.apps.googleusercontent.com.json"
)

# Ad Manager API scope
SCOPES = ["https://www.googleapis.com/auth/admanager"]

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "secrets", "gam-credentials.json")

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
creds = flow.run_local_server(port=0, open_browser=True)

os.makedirs(os.path.dirname(CREDENTIALS_FILE), exist_ok=True)
with open(CREDENTIALS_FILE, "w") as f:
    json.dump({
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "refresh_token": creds.refresh_token,
        "token_uri": "https://oauth2.googleapis.com/token",
    }, f, indent=2)

print(f"\nCredentials saved to {os.path.abspath(CREDENTIALS_FILE)}")
