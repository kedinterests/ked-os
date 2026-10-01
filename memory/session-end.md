---
name: KED-OS End of Session Routine
description: Steps to follow at the end of every KED-OS session — run without being asked
---

# KED-OS End of Session Routine

Run without being asked at the end of every session. Follow the checklist in order.

## 1. Active Project Checkpoint

If any active KED project was touched this session, before closing out:

- **What is the next action?** (specific, not vague)
- **Who owns it?** (Chris, Kenny)
- **Does it need a reminder?** If yes, create an Apple Reminder on Hot List with a due date.

```bash
osascript -e 'tell application "Reminders" to tell list "Hot List" to make new reminder with properties {name:"REMINDER TEXT", due date:date "Month Day, Year HH:MM:SS AM/PM"}'
```

Available lists: Reminders, Hot List, Family, WWWS, Family (with warning icon), ~Up Next Tasks~. Default to **Hot List** unless specified otherwise.

## 2. Archive TASKS.md

Move any completed items in the Done/Completed section older than 7 days to `memory/tasks-archive.md` (append with session date). Keep `TASKS.md` focused on active work.

## 3. Log Decisions → `decisions/`

If a non-trivial decision was made this session (architecture, scope, vendor choice, tooling, project direction), log it to `decisions/YYYY-MM-DD-slug.md`:

```markdown
# [Decision Title]

**Date:** YYYY-MM-DD
**What:** [one-sentence summary of what was decided]
**Why:** [the reason — constraint, goal, stakeholder ask]
**Alternatives considered:** [what was rejected and why]
```

Create the `decisions/` folder if it doesn't yet exist.

## 4. Log Dev Notes → `dev/`

If exploratory work, debugging notes, or research that doesn't belong to a specific project came up, append to `dev/YYYY-MM-DD-topic.md`. Create the `dev/` folder if it doesn't exist.

## 5. Save Code → Project Snippets

Any reusable code written this session gets saved to the relevant project:

- Internal/KED project code: `internal/[project]/code/ked-YYYY-MM-DD-desc.[ext]`
- Cross-project utility: `internal/_shared/code/ked-YYYY-MM-DD-desc.[ext]`

Log each in `memory/snippet-index.md` (create if missing) with one line: `- [date] [path] — [one-line purpose, tags]`.

## 6. Update Memory

If anything new was learned this session that should persist:

- New KED, oil & gas, or industry term → `memory/glossary.md`
- New fact about Kenny, his preferences, or how he likes to work → `memory/people/kenny-dubose.md`
- New company / context about KED Interests itself → `memory/context/company.md`
- Reusable workflow or tool reference (CLI, API key location, etc.) → `memory/reference_*.md`

Do not duplicate. If a memory exists, update in place.

## 7. Optimization Observations

Friction noticed this session — slow lookups, repeated patterns, token bloat, awkward workflows — append one line to `memory/optimization-observations.md` (create if missing). One line per observation; later sessions will batch-fix.

## 8. Radar Check

If `memory/radar.md` was last reviewed > 3–4 weeks ago, flag it for review next session. Do not auto-run radar.

## 9. Commit and Push to Main

If there are uncommitted changes:

```bash
git add -A
git commit -m "[one-line summary of session work]"
```

- If on a non-main branch: `git checkout main && git merge [branch] && git push origin main`
- If already on main: `git push origin main`

Never use `--no-verify` or skip hooks. Investigate hook failures rather than bypassing.

## End

Session complete. KED-OS state is durable — next session will pick up cleanly.
