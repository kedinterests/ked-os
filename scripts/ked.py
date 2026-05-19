#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

def load_index():
    """Load the KED-OS index."""
    index_path = Path.cwd() / 'ked-os-index.json'

    if not index_path.exists():
        print("Error: ked-os-index.json not found. Run 'python3 scripts/migrate.py' first.")
        sys.exit(1)

    with open(index_path, 'r') as f:
        return json.load(f)

def cmd_stats():
    """Show statistics about KED-OS."""
    index = load_index()

    print("KED-OS Overview")
    print("=" * 40)
    print(f"Projects:       {len(index['projects'])}")
    print(f"Skills:         {len(index['skills'])}")
    print(f"Core docs:      {len(index['docs'])}")
    print(f"Memory files:   {len(index['memory'])}")
    print()

    stacks = {}
    for proj in index['projects']:
        stack = proj.get('stack', 'unknown')
        stacks[stack] = stacks.get(stack, 0) + 1

    print("By Stack:")
    for stack, count in sorted(stacks.items()):
        print(f"  {stack}: {count}")
    print()

    statuses = {}
    for proj in index['projects']:
        status = proj.get('status', 'unknown')
        statuses[status] = statuses.get(status, 0) + 1

    print("Project Status:")
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")

def cmd_projects(stack=None):
    """List projects, optionally filtered by stack."""
    index = load_index()

    projects = index['projects']
    if stack:
        projects = [p for p in projects if stack.lower() in p.get('stack', '').lower()]

    if not projects:
        print("No projects found.")
        return

    print("Projects:")
    print("-" * 60)
    for proj in sorted(projects, key=lambda p: p['name']):
        print(f"  {proj['name']}")
        print(f"    Stack:  {proj.get('stack', 'unknown')}")
        print(f"    Status: {proj.get('status', 'unknown')}")
        print(f"    Owner:  {proj.get('owner', 'unknown')}")
        if proj.get('repo'):
            print(f"    Repo:   {proj['repo']}")
        print()

def cmd_skills():
    """List all skills."""
    index = load_index()

    skills = index['skills']
    if not skills:
        print("No skills found.")
        return

    print("Available Skills:")
    print("-" * 60)
    for skill in sorted(skills, key=lambda s: s['name']):
        print(f"  {skill['name']}")
        if skill.get('description'):
            print(f"    {skill['description']}")
        print()

def cmd_query(item_type, **filters):
    """Query the index."""
    index = load_index()

    if item_type == 'projects':
        stack = filters.get('stack')
        cmd_projects(stack)
    elif item_type == 'skills':
        cmd_skills()
    elif item_type == 'stats':
        cmd_stats()
    else:
        print(f"Unknown query type: {item_type}")
        sys.exit(1)

def cmd_search(query):
    """Search projects and skills by name."""
    index = load_index()
    query_lower = query.lower()

    results = []

    for proj in index['projects']:
        if query_lower in proj['name'].lower() or query_lower in proj.get('repo', '').lower():
            results.append(('project', proj))

    for skill in index['skills']:
        if query_lower in skill['name'].lower():
            results.append(('skill', skill))

    if not results:
        print(f"No results for: {query}")
        return

    print(f"Search results for '{query}':")
    print("-" * 60)
    for item_type, item in results:
        print(f"  [{item_type}] {item['name']}")
        if item.get('description'):
            print(f"    {item['description']}")
        print()

def usage():
    print("""KED-OS Index Query Tool

Usage:
  python3 scripts/ked.py stats                    Show KED-OS statistics
  python3 scripts/ked.py query projects           List all projects
  python3 scripts/ked.py query projects --stack Astro
                                                  List projects using Astro
  python3 scripts/ked.py query skills             List all skills
  python3 scripts/ked.py search <term>            Search projects and skills
  python3 scripts/ked.py query snippets --tag <tag>
                                                  Find snippets with tag (future)

Examples:
  python3 scripts/ked.py stats
  python3 scripts/ked.py query projects --stack Astro
  python3 scripts/ked.py search mineralwise
""")

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'stats':
        cmd_stats()
    elif cmd == 'query':
        if len(sys.argv) < 3:
            usage()
            sys.exit(1)
        item_type = sys.argv[2]

        filters = {}
        i = 3
        while i < len(sys.argv):
            if sys.argv[i].startswith('--'):
                key = sys.argv[i][2:]
                if i + 1 < len(sys.argv):
                    filters[key] = sys.argv[i + 1]
                    i += 2
                else:
                    i += 1
            else:
                i += 1

        cmd_query(item_type, **filters)
    elif cmd == 'search':
        if len(sys.argv) < 3:
            print("Usage: python3 scripts/ked.py search <term>")
            sys.exit(1)
        cmd_search(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        usage()
        sys.exit(1)

if __name__ == '__main__':
    main()
