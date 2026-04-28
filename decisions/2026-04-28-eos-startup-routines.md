# EOS and Session Start Routines for KED-OS

**Date:** 2026-04-28
**What:** Added `memory/session-start.md` and rewrote `memory/session-end.md` to mirror brilliant-os's routines, adapted for KED context (single client, simpler structure, no Novamira/teammates). Added a `SessionStart` git-fetch hook to `.claude/settings.json`. Replaced the inline session-start block in `CLAUDE.md` with a one-line pointer to the new file, matching how session-end was already referenced.
**Why:** Sessions need durable startup and shutdown discipline so context, decisions, and code don't get stranded between sessions. Brilliant-os already has this pattern working; KED-OS should use the same shape so muscle memory transfers between the two repos.
**Alternatives considered:** Embedding both routines inline in CLAUDE.md — rejected because CLAUDE.md is already loaded into every session and bloats the context window. Routines belong in files that are read on demand.
