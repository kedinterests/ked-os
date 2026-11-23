#!/usr/bin/env python3
"""
One-time OAuth flow to get a Google Analytics 4 refresh token.
Reuses the existing `claude-gam` OAuth client (same one GAM uses).
Run: python3 scripts/ga-auth.py
"""

import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET_FILE = os.path.expanduser(
    "~/Downloads/client_secret_896537630194-oc56mk0ucfdqsrg5a3a25bg97hp74hk5.apps.googleusercontent.com.json"
)

# Read-only access to GA4 reporting and property metadata
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "secrets", "ga-credentials.json")

if not os.path.exists(CLIENT_SECRET_FILE):
    raise SystemExit(
        f"Client secret not found at:\n  {CLIENT_SECRET_FILE}\n\n"
        "Download it again from Google Cloud Console > APIs & Services > Credentials\n"
        "(project: claude-gam), or edit CLIENT_SECRET_FILE at the top of this script."
    )

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

os.chmod(CREDENTIALS_FILE, 0o600)

print(f"\nCredentials saved to {os.path.abspath(CREDENTIALS_FILE)}")
print("Next: python3 scripts/ga-test.py")
