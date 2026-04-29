---
name: KED-OS Bolstering Work
description: Prioritized list of fixes and gaps to address before doing real KED work — surface this at every session start until done
type: project
---

KED-OS has several broken or misaligned pieces that need fixing. Surface this at the top of every session until all items are checked off.

**Why:** Assessed 2026-04-28. Most of this is initialization debt — the system was seeded from BWW patterns but not fully adapted for KED.

**How to apply:** Before taking on new KED work in a session, ask Chris if he wants to knock out any of these. Mark items done here as they're completed.

---

## Priority 1 — Broken workflows (do these first)

- [ ] Build `scripts/ked.py`, `ked-os-index.json`, and `scripts/migrate.py` — CLAUDE.md tells every session to use these for discovery, but none of them exist. The entire index-first lookup workflow is dead without them.
- [ ] Create `internal/news-tracking/index.md` — the industry news skill writes here on Step 4; the folder doesn't exist yet.

## Priority 2 — BWW transplants that need KED adaptation

- [ ] Rewrite `skills/project-initialization/SKILL.md` — still says "Claude Co-Work (BWW)", references `core/standard-stack.md` (wrong path), and creates a folder structure that doesn't match KED-OS's `internal/[name]/` pattern.
- [ ] Adapt `skills/voice-profile/SKILL.md` — says "BWW" throughout; output paths reference `projects/[name]/` which doesn't exist in KED-OS. Should route to `internal/[name]/` or `memory/people/`.

## Priority 3 — Cleanup

- [ ] Fix `.claude/settings.json` — remove `max_tokens`, `temperature`, `status_line` (not valid Claude Code keys; runtime ignores them).
- [ ] Remove Life OS reference from `memory/people/chris-malone.md` — violates KED-OS isolation rule in CLAUDE.md.
- [ ] Clear placeholder content from `TASKS.md` (still has "Task 1, Task 2, Task 3").
