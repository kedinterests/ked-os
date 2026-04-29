---
name: KED-OS Session Start Routine
description: Steps to follow at the start of every KED-OS session — classify, orient, surface what matters
---

# KED-OS Session Start Routine

Run at the start of every session, before doing other work. Goal: pick the right model, load only what's needed, and surface anything blocking.

A `.claude/settings.json` SessionStart hook already runs `git fetch origin` asynchronously, so remote state is fresh before this routine runs.

## 1. Detect the Current User

```bash
git config user.email
```

| Email | Who | Notes |
|-------|-----|-------|
| chris@m11design.com | Chris | Developer, project lead. Personal context lives in chris-os if connected. |
| kenny@kedinterests.com | Kenny | Founder. Voice profile: `memory/people/kenny-dubose.md`. |

If the email is unknown, ask before assuming.

## 2. Classify the Session — Pick the Right Model

**Default: Sonnet.** Always prompt Chris to downgrade or upgrade based on the task at hand — do not silently proceed on the wrong model.

**Model routing:**

- **Haiku:** task management, TASKS.md updates, note logging, file organization, quick lookups, status updates, radar reviews. Suggest downgrading from Sonnet for these.
- **Sonnet (default):** code, architecture, security review, proposals, complex troubleshooting, anything requiring judgment.
- **Opus:** suggest upgrading from Sonnet only when the task warrants it (deep architectural reasoning, complex multi-file refactors, hard debugging).

**First response in every session: assess the model and prompt for a switch if the current one doesn't fit.** If the prompt is ambiguous, ask what we're doing before recommending.

## 3. Load Only What the Session Requires

Skills add context overhead — invoke them only when their workflow adds genuine value. For direct file operations (reading TASKS.md, logging notes, updating decisions), use Read/Edit directly.

| Session type | Load |
|---|---|
| Quick task / admin | Nothing beyond CLAUDE.md |
| KED code / snippet | `core/ked-stack.md` + `core/astro-patterns.md` (lite) |
| Architecture / security | `core/ked-stack.md` (full) + Kenny's profile |
| Industry news prep | Nothing extra — `skills/ked-industry-news/` handles its own context |
| Proposal / copy / client-facing writing | `memory/people/kenny-dubose.md` for voice |
| New project | Create from `internal/_template/` first |

If writing code: query snippets first (`python3 scripts/ked.py query snippets --tag X`); only load the file when a match exists.

## 4. Active Project Awareness

Glance at `TASKS.md` and any active project's `notes/` folder to surface:

- In-flight work that was paused last session
- Anything blocked or waiting on Kenny
- Reminders or deadlines coming up this week

If something needs Kenny's input or has a deadline, surface it before diving into the new request.

## 5. Radar Staleness

If `memory/radar.md` was last updated > 3–4 weeks ago, flag it once at the top of the session. Do not auto-run radar.

## 6. Memory Sweep

Skim `memory/MEMORY.md` for any entries relevant to the opening prompt. Memory may be stale — verify against current code before acting on it.

## End of Routine

Confirm the session is on the right model, the right context is loaded, and nothing critical is being ignored. Then proceed with the user's request.
