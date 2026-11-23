#!/bin/bash
# Launch wrapper for the google-search-console-ked MCP server.
#
# The GUI-launched Claude app does not source the shell profile, so credentials
# are loaded here from .env (this folder, gitignored, mode 600) at launch time.
#
# Usage:      ./run-mcp.sh [server-args]
# Smoke test: ./run-mcp.sh --ping
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$DIR/.env" ]; then
  echo "run-mcp.sh: $DIR/.env not found. See SETUP.md." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1091
. "$DIR/.env"
set +a

exec "$DIR/.venv/bin/python" "$DIR/server.py" "$@"
