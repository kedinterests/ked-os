# KED-OS Index System

The KED-OS index is a comprehensive catalog of all projects, skills, docs, and memory files in the system. It's generated automatically and kept up to date via git hooks.

## Files

- `ked-os-index.json` — The complete index (auto-generated)
- `scripts/migrate.py` — Regenerates the index from the file system
- `scripts/ked.py` — Query tool for searching and exploring

## Usage

### Regenerate the index (after adding projects/skills)

```bash
python3 scripts/migrate.py
```

This scans the entire KED-OS directory and rebuilds the index. Run this after:
- Adding a new project to `internal/`
- Adding a new skill to `skills/`
- Adding core docs to `core/`
- Adding memory files to `.claude/memory/`

### Query the index

```bash
# Overview of KED-OS
python3 scripts/ked.py stats

# List all projects
python3 scripts/ked.py query projects

# List projects using Astro
python3 scripts/ked.py query projects --stack Astro

# List all skills
python3 scripts/ked.py query skills

# Search projects and skills
python3 scripts/ked.py search mineralwise
python3 scripts/ked.py search "code verification"
```

## How it works

1. **migrate.py** scans the directory structure:
   - `internal/*/profile.md` for projects
   - `skills/*/SKILL.md` for skills
   - `core/*.md` for documentation
   - `.claude/memory/*.md` for memory files

2. **ked.py** loads the index and provides query commands

3. The index is **not** committed to git (it's regenerated on each session)

## Integration with Claude Code

When you load ked-os in Claude Code:
1. The index is scanned on first load
2. Use `python3 scripts/ked.py` commands to discover projects before loading files
3. On session end, run `migrate.py` if anything was added

## Example workflow

```bash
# Add a new project
mkdir internal/new-project
cp internal/_template/profile.md internal/new-project/

# Edit the profile
# ... fill in project details ...

# Regenerate the index to include it
echo "y" | python3 scripts/migrate.py

# Verify it's in the index
python3 scripts/ked.py query projects
```
