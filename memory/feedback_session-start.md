---
name: Run session-start at the top of every session
description: Chris expects the session-start routine to run automatically at the beginning of every KED-OS session, without being asked.
type: feedback
---

Always run `memory/session-start.md` at the very top of every session, before any other work. Do not wait for the user to prompt it.

**Why:** Chris explicitly corrected this on 2026-04-28. The CLAUDE.md instruction is mandatory, not optional.

**How to apply:** The first thing in any KED-OS session is to read `memory/session-start.md` and execute its steps: detect user, classify model, check TASKS.md, check radar staleness, skim MEMORY.md. Then report findings before proceeding with the user's request.
