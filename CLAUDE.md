# KED-OS

## People

| Who | Role |
|-----|------|
| Chris | chris@m11design.com — developer and project lead |
| Kenny | kenny@kedinterests.com — founder, KED Interests |

Profiles: `memory/people/` | Glossary: `memory/glossary.md` | Company: `memory/context/company.md`

## Key Terms

| Term | Meaning |
|------|---------|
| KED | KED Interests — oil & gas energy sector web development |
| Astro | Static site generator for KED web projects |
| Discourse | Community forum platform for KED projects |
| Vibe | Hand-coded sites built to Vibe specs |

New KED term? Add to `memory/glossary.md` before end of session.

## Output Rules (Always Active)

- No preamble, no intro clauses, no emojis
- Prose over bullets in conversation
- Complete code always — never partial diffs
- No code explanations unless asked
- No CSS comments unless asked
- Ask rather than assume
- Never use em dashes or en dashes — use commas, colons, semicolons, or periods instead

## Code Defaults (Always Active)

- JavaScript/TypeScript for Astro projects (no legacy jQuery unless required)
- Modern Node.js (18+)
- Snippets: copy-paste ready, no preamble
- Production is fragile — ask before touching it

## Writing for Kenny

Before any client-facing copy, emails, proposals, or content written on Kenny's behalf: load `memory/people/kenny-dubose.md`.

## Session Start — Classify First

**Model routing — follow strictly:**

- **Haiku:** task management, note logging, quick lookups, status updates, project organization
- **Sonnet:** Code, architecture, complex troubleshooting, anything requiring judgment

**First response: check the model.** If on wrong model for the task, flag it and suggest switching.

**Load only what the session requires:**

| Session type | Load |
|---|---|
| Quick task / admin | Nothing beyond CLAUDE.md |
| KED code / snippet | `core/ked-stack.md` + `core/astro-patterns.md` |
| Architecture / security | `core/ked-stack.md` (full) + Kenny's profile |
| Industry news prep | Nothing extra — skill handles context |
| New project | Create from `internal/_template/` first |

If writing code: query snippets first (`python3 scripts/ked.py query snippets --tag X`), then load the file only if a match is found.
Radar cadence: if `memory/radar.md` last reviewed > 3–4 weeks, flag it.

## KED-OS Index (Token-Efficient Lookups)

`ked-os-index.json` + `scripts/ked.py` — use these for discovery before loading any files.

**Use the index first. Load files only when you need the full content.**

```bash
# What stack does this project use?
python3 scripts/ked.py query projects --stack "Astro"

# Has this been built before?
python3 scripts/ked.py query snippets --tag drilling

# Find anything related to a topic
python3 scripts/ked.py search "mineral rights"

# Overview of all projects
python3 scripts/ked.py stats
```

Regenerate the index after adding/changing projects or snippets:
```bash
echo "y" | python3 scripts/migrate.py
```

## Skills

**How to invoke local skills:** Read the `SKILL.md` file in the skill's folder and follow its instructions.

Use `python3 scripts/ked.py query skills` to see all available skills.

| Folder | When to use |
|--------|-------------|
| `skills/code-verification/` | Three-pass code verification |
| `skills/security-audit/` | Code security audit |
| `skills/project-initialization/` | New project folder setup |
| `skills/ked-industry-news/` | Weekly O&G / mineral rights / drilling news prep |
| `skills/voice-profile/` | Voice profile |

## Projects

- Project work: `internal/[name]/` — `profile.md`, `notes/`, tasks
- Templates: `internal/_template/`

## Active Project Checkpoint

**Mandatory.** When work on any active project concludes during a session, before moving to the next topic:

1. **What is the next action?** (specific, not vague)
2. **Who owns it?** (Chris, Kenny)
3. **Does it need a reminder?** If yes, create an Apple Reminder on Hot List with a due date.

Apple Reminders access via AppleScript:
```bash
osascript -e 'tell application "Reminders" to tell list "Hot List" to make new reminder with properties {name:"REMINDER TEXT", due date:date "Month Day, Year HH:MM:SS AM/PM"}'
```

Do not skip this checkpoint.

## End of Session

Follow `memory/session-end.md` — run without being asked.

## Cross-OS Awareness

KED-OS knows about:
- **Brilliant OS** — reference for patterns, structure, and shared context (read-only)

KED-OS is isolated from:
- **Life OS** — Chris's personal work (not referenced from KED-OS)
- **Brilliant OS** does not know about KED-OS (from Brilliant OS perspective)
