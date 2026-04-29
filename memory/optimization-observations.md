# Optimization Observations

Friction noticed during sessions. One line per observation. Batch-fix later.

- 2026-04-28 — `.claude/settings.json` contains non-standard Claude Code keys (`max_tokens`, `temperature`, `status_line`) that the runtime ignores. Either remove or replace with the supported equivalents (e.g., `statusLine` config) on a future cleanup pass.
- 2026-04-29 — CLAUDE.md references `scripts/migrate.py` for index regeneration, but that file was never created. Update CLAUDE.md to point to `scripts/ked.py` directly for index queries; remove the migrate.py reference.
