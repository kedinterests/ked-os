"""One-time OAuth login for the KED Search Console + Analytics connectors.

Reads GSC_CLIENT_ID and GSC_CLIENT_SECRET from .env, opens a browser for the
Google sign-in (sign in as chris@kedinterests.com), then writes:

  .env          GSC_REFRESH_TOKEN=...            used by server.py
  ga-adc.json   authorized_user credentials      used by google-analytics-ked

Neither value is printed to the terminal.

Usage:
  .venv/bin/python get_token.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
ADC_FILE = ROOT / "ga-adc.json"
load_dotenv(ENV_FILE)

SCOPES = [
    "https://www.googleapis.com/auth/webmasters",
    "https://www.googleapis.com/auth/analytics.readonly",
]


def _write_env_key(key: str, value: str) -> None:
    lines = ENV_FILE.read_text().splitlines() if ENV_FILE.exists() else []
    out, replaced = [], False
    for line in lines:
        if line.startswith(f"{key}="):
            out.append(f"{key}={value}")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(f"{key}={value}")
    ENV_FILE.write_text("\n".join(out) + "\n")


def main() -> None:
    client_id = os.environ.get("GSC_CLIENT_ID")
    client_secret = os.environ.get("GSC_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("ERROR: set GSC_CLIENT_ID and GSC_CLIENT_SECRET in .env first (see SETUP.md).")
        sys.exit(1)

    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        },
        scopes=SCOPES,
    )
    creds = flow.run_local_server(
        port=0,
        prompt="consent",
        access_type="offline",
        authorization_prompt_message=(
            "Opening a browser to authorize the KED Search Console + Analytics connectors. "
            "Sign in as chris@kedinterests.com."
        ),
        success_message="Authorized. Close this tab and return to the terminal.",
    )
    if not creds.refresh_token:
        print("ERROR: Google returned no refresh_token. Remove this app under myaccount.google.com/permissions and run again.")
        sys.exit(1)

    _write_env_key("GSC_REFRESH_TOKEN", creds.refresh_token)
    ADC_FILE.write_text(
        json.dumps(
            {
                "type": "authorized_user",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": creds.refresh_token,
            },
            indent=2,
        )
        + "\n"
    )
    os.chmod(ADC_FILE, 0o600)
    os.chmod(ENV_FILE, 0o600)

    print()
    print(f"Authorized. Refresh token written to .env ({len(creds.refresh_token)} chars) and ga-adc.json.")
    print("Next: ./run-mcp.sh --ping   then   ./register.sh")


if __name__ == "__main__":
    main()
