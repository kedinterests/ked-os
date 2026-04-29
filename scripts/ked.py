#!/usr/bin/env python3
"""KED-OS index query tool."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
INDEX_PATH = ROOT / "ked-os-index.json"


def load_index():
    with open(INDEX_PATH) as f:
        return json.load(f)


def cmd_query(args):
    index = load_index()
    section = args.section

    if section not in index:
        print(f"Unknown section: {section}. Available: {', '.join(index.keys())}")
        sys.exit(1)

    items = index[section]
    if not isinstance(items, list):
        print(json.dumps(items, indent=2))
        return

    results = items

    if section == "projects":
        if args.stack:
            term = args.stack.lower()
            results = [p for p in results if any(term in s.lower() for s in p.get("stack", []))]
        if args.status:
            results = [p for p in results if p.get("status") == args.status]
        if args.tag:
            results = [p for p in results if args.tag.lower() in [t.lower() for t in p.get("tags", [])]]

    if section == "snippets":
        if args.tag:
            results = [s for s in results if args.tag.lower() in [t.lower() for t in s.get("tags", [])]]

    if not results:
        print("No results.")
        return

    for item in results:
        _print_item(section, item)


def _print_item(section, item):
    if section == "projects":
        status = item.get("status", "")
        stack = ", ".join(item.get("stack", []))
        repo = item.get("repo") or "(no remote)"
        local = item.get("local") or "(not cloned)"
        print(f"\n[{item['id']}] {item['name']}  [{status}]")
        print(f"  Stack:  {stack}")
        print(f"  Repo:   {repo}")
        print(f"  Local:  {local}")
        print(f"  Path:   {item.get('path', '')}")
        print(f"  {item.get('description', '')}")
        if item.get("tags"):
            print(f"  Tags:   {', '.join(item['tags'])}")
    elif section == "snippets":
        print(f"\n[{item['id']}] {item.get('name', item['id'])}")
        print(f"  {item.get('description', '')}")
        if item.get("tags"):
            print(f"  Tags: {', '.join(item['tags'])}")
        if item.get("path"):
            print(f"  File: {item['path']}")
    elif section == "skills":
        print(f"\n[{item['id']}] {item['name']}")
        print(f"  When: {item.get('when', '')}")
        print(f"  Path: {item.get('path', '')}")
    elif section == "core":
        print(f"\n[{item['id']}] {item['name']}")
        print(f"  {item.get('description', '')}")
        print(f"  Path: {item.get('path', '')}")
    elif section == "memory":
        print(f"\n[{item['id']}] {item['name']}")
        print(f"  {item.get('description', '')}")
        print(f"  Path: {item.get('path', '')}")
    elif section == "decisions":
        print(f"\n[{item['id']}]  {item.get('date', '')}  {item.get('summary', '')}")
        print(f"  Path: {item.get('path', '')}")
    else:
        print(json.dumps(item, indent=2))


def cmd_search(args):
    index = load_index()
    term = args.term.lower()
    found = False

    for section in ["projects", "snippets", "skills", "core", "memory", "decisions"]:
        items = index.get(section, [])
        if not isinstance(items, list):
            continue
        for item in items:
            blob = json.dumps(item).lower()
            if term in blob:
                _print_item(section, item)
                found = True

    if not found:
        print(f"No results for '{args.term}'.")


def cmd_stats(args):
    index = load_index()
    projects = index.get("projects", [])
    snippets = index.get("snippets", [])
    skills = index.get("skills", [])

    by_status = {}
    for p in projects:
        s = p.get("status", "unknown")
        by_status.setdefault(s, []).append(p["name"])

    print(f"\nKED-OS Index  (updated {index['meta']['updated']})")
    print(f"  Projects : {len(projects)}")
    for status, names in sorted(by_status.items()):
        print(f"    {status}: {', '.join(names)}")
    print(f"  Snippets : {len(snippets)}")
    print(f"  Skills   : {len(skills)}")
    print(f"  Decisions: {len(index.get('decisions', []))}")

    stacks = {}
    for p in projects:
        for s in p.get("stack", []):
            stacks[s] = stacks.get(s, 0) + 1
    if stacks:
        print("\n  Stack frequency:")
        for s, count in sorted(stacks.items(), key=lambda x: -x[1]):
            print(f"    {s}: {count}")

    not_cloned = [p["name"] for p in projects if not p.get("local")]
    if not_cloned:
        print(f"\n  Not cloned locally: {', '.join(not_cloned)}")


def main():
    parser = argparse.ArgumentParser(description="KED-OS index query tool")
    sub = parser.add_subparsers(dest="cmd")

    q = sub.add_parser("query", help="Query a section of the index")
    q.add_argument("section", choices=["projects", "snippets", "skills", "core", "memory", "decisions"])
    q.add_argument("--stack", help="Filter projects by stack term")
    q.add_argument("--status", help="Filter projects by status")
    q.add_argument("--tag", help="Filter by tag")

    s = sub.add_parser("search", help="Full-text search across all sections")
    s.add_argument("term")

    sub.add_parser("stats", help="Overview of all projects and sections")

    args = parser.parse_args()

    if args.cmd == "query":
        cmd_query(args)
    elif args.cmd == "search":
        cmd_search(args)
    elif args.cmd == "stats":
        cmd_stats(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
