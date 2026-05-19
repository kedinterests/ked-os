#!/usr/bin/env python3
import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

def parse_frontmatter(content):
    """Parse YAML-style frontmatter from markdown."""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    fm_text = parts[1]
    body = parts[2].strip()
    fm = {}

    for line in fm_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            fm[key] = value

    return fm, body

def scan_projects(base_path):
    """Scan internal/ directory for project profiles."""
    projects = []
    internal_path = Path(base_path) / 'internal'

    if not internal_path.exists():
        return projects

    for project_dir in internal_path.iterdir():
        if project_dir.is_dir() and project_dir.name.startswith('_'):
            continue

        profile_path = project_dir / 'profile.md'
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                content = f.read()

            fm, body = parse_frontmatter(content)

            project = {
                'name': fm.get('name', project_dir.name),
                'path': f"internal/{project_dir.name}",
                'status': fm.get('status', 'unknown'),
                'stack': fm.get('stack', 'unknown'),
                'owner': fm.get('owner', 'unknown'),
                'repo': fm.get('repo', ''),
                'location': fm.get('location', ''),
                'type': 'project',
                'indexed': datetime.now().isoformat()
            }
            projects.append(project)

    return projects

def scan_skills(base_path):
    """Scan skills/ directory for available skills."""
    skills = []
    skills_path = Path(base_path) / 'skills'

    if not skills_path.exists():
        return skills

    for skill_dir in skills_path.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / 'SKILL.md'
        if skill_md.exists():
            with open(skill_md, 'r') as f:
                content = f.read()

            fm, body = parse_frontmatter(content)

            # Extract first line as description if no fm description
            desc_match = re.match(r'^# (.+)', body, re.MULTILINE)
            description = fm.get('description', desc_match.group(1) if desc_match else '')

            skill = {
                'name': skill_dir.name,
                'path': f"skills/{skill_dir.name}",
                'description': description,
                'type': 'skill'
            }
            skills.append(skill)

    return skills

def scan_core(base_path):
    """Scan core/ directory for documentation."""
    docs = []
    core_path = Path(base_path) / 'core'

    if not core_path.exists():
        return docs

    for doc_file in core_path.glob('*.md'):
        with open(doc_file, 'r') as f:
            content = f.read()

        fm, body = parse_frontmatter(content)
        title = fm.get('name', fm.get('title', doc_file.stem))

        doc = {
            'name': title,
            'path': f"core/{doc_file.name}",
            'description': fm.get('description', ''),
            'type': 'doc'
        }
        docs.append(doc)

    return docs

def scan_memory(base_path):
    """Scan .claude/memory/ for memory files."""
    memories = []
    memory_path = Path(base_path) / '.claude' / 'memory'

    if not memory_path.exists():
        return memories

    for mem_file in memory_path.glob('*.md'):
        if mem_file.name == 'MEMORY.md':
            continue

        with open(mem_file, 'r') as f:
            content = f.read()

        fm, body = parse_frontmatter(content)

        memory = {
            'name': fm.get('name', mem_file.stem),
            'path': f".claude/memory/{mem_file.name}",
            'description': fm.get('description', ''),
            'type': fm.get('metadata', {}).get('type') if isinstance(fm.get('metadata'), dict) else 'memory'
        }
        memories.append(memory)

    return memories

def generate_index(base_path):
    """Generate complete KED-OS index."""
    index = {
        'meta': {
            'version': '1.0',
            'generated': datetime.now().isoformat(),
            'base': base_path
        },
        'projects': scan_projects(base_path),
        'skills': scan_skills(base_path),
        'docs': scan_core(base_path),
        'memory': scan_memory(base_path)
    }

    return index

def main():
    base_path = os.getcwd()

    if not os.path.exists('CLAUDE.md'):
        print("Error: Not in KED-OS root directory (CLAUDE.md not found)")
        sys.exit(1)

    print("Scanning KED-OS structure...")
    index = generate_index(base_path)

    print(f"Found:")
    print(f"  - {len(index['projects'])} projects")
    print(f"  - {len(index['skills'])} skills")
    print(f"  - {len(index['docs'])} core docs")
    print(f"  - {len(index['memory'])} memory files")

    # Write index
    index_path = Path(base_path) / 'ked-os-index.json'
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)

    print(f"\nIndex written to: {index_path}")
    print("Done.")

if __name__ == '__main__':
    main()
