# GAM API Setup and Reporting Infrastructure

**Date:** 2026-06-17
**What:** Connected Google Ad Manager API (v1) for network 6933594 via OAuth 2.0. Built reporting scripts for YTD all-advertiser summaries and single-advertiser client PDFs. Created a `gam-reporting` skill.
**Why:** Kenny needed a way to pull performance data programmatically and generate client-facing reports without manual GAM UI exports.
**Alternatives considered:** Service account auth (requires domain-wide delegation, more complex); manual CSV exports from GAM UI (not repeatable).

## Key implementation details
- Auth type: OAuth 2.0 installed app (client secret JSON from Google Cloud project `claude-gam`)
- Credentials stored in `secrets/gam-credentials.json` (gitignored)
- Re-auth script: `scripts/gam-auth.py`
- Scope: `https://www.googleapis.com/auth/admanager`
- Report flow: POST /reports → POST :run → GET operation (poll) → GET {resultPath}:fetchRows
- `fetchRows` is a GET, not POST — common error
- `MONTH_YEAR` dimension returns sequential integer month codes (not YYYYMM) — map manually
- Line items v1 API: read-only, no targeting fields, no create/update — must use GAM UI for trafficking
