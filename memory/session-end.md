---
name: KED-OS Session End Routine
description: Steps to follow at the end of every KED-OS session
---

# KED-OS Session End Routine

Run this routine at the end of every session. Follow the checklist in order.

## 1. Active Project Checkpoint

If you worked on an active KED project:
- What is the next action? (specific, not vague)
- Who owns it? (Chris, Kenny)
- Does it need a reminder? If yes, create an Apple Reminder on Hot List

```bash
osascript -e 'tell application "Reminders" to tell list "Hot List" to make new reminder with properties {name:"REMINDER TEXT", due date:date "Month Day, Year HH:MM:SS AM/PM"}'
```

## 2. Update Memory

If you learned something new about KED, Kenny, the industry, or workflows:
- Update or add to `memory/context/`
- Update `memory/glossary.md` if new terms came up
- Update `memory/people/` if preferences or context changed

## 3. Check Radar

If `memory/radar.md` last updated > 3–4 weeks ago, flag it for review next session.

## 4. Task Management

If using `TASKS.md` for the session, review:
- Are all completed tasks marked `completed`?
- Do any tasks need carryover to next session?

## 5. Git Commit (if applicable)

If working on active projects with changes:
- Stage: `git add .`
- Commit with clear message: `git commit -m "..."`
- Push if remote tracking: `git push`

## End

Session complete. KED-OS ready for next work.
