#!/bin/bash
# Registers the two KED Google connectors with Claude Code (user scope, so they
# are available in every project, not written into any repo).
#
#   google-search-console-ked   server.py in this folder
#   google-analytics-ked        Google's analytics-mcp, pointed at ga-adc.json
#
# Run once, after get_token.py has succeeded.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$DIR/.env" ] || [ ! -f "$DIR/ga-adc.json" ]; then
  echo "register.sh: run get_token.py first (needs .env and ga-adc.json)." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1091
. "$DIR/.env"
set +a

if [ -z "$GOOGLE_PROJECT_ID" ]; then
  echo "register.sh: GOOGLE_PROJECT_ID is not set in .env (the Cloud project that owns the OAuth client)." >&2
  exit 1
fi

claude mcp remove --scope user google-search-console-ked >/dev/null 2>&1 || true
claude mcp remove --scope user google-analytics-ked >/dev/null 2>&1 || true

claude mcp add --scope user google-search-console-ked -- "$DIR/run-mcp.sh"

claude mcp add --scope user google-analytics-ked \
  -e "GOOGLE_APPLICATION_CREDENTIALS=$DIR/ga-adc.json" \
  -e "GOOGLE_PROJECT_ID=$GOOGLE_PROJECT_ID" \
  -- pipx run analytics-mcp

echo
echo "Registered. Restart the Claude session, then ask for list_sites on google-search-console-ked."
