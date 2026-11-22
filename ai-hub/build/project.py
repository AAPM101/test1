#!/usr/bin/env python3
"""Project provenance and sync helper.

  project.py new <name> --tool T [--title ...] [--profile bsi|personal|none] [--sync-to claude,chatgpt]
  project.py log <name> --tool T --note "..."
  project.py decide <name> --tool T --what "..." --why "..."
  project.py export <name> --tool T
  project.py import <name> --tool T
"""
import argparse
import hashlib
import re
import shutil

from common import (PROJECTS, add_history, append, die, fmt_list, get_field, now, parse_list,
                    project_dir, read, set_field, today, write)

SKIP = {"MANIFEST.md", ".gitkeep"}


def touch(d, tool, action):
    """Record provenance: updated_by/at plus a history entry."""
    p = d / "project.yaml"
    t = read(p)
    t = set_field(t, "updated_by", tool)
    t = set_field(t, "updated_at", today())
    t = add_history(t, today(), tool, action)
    write(p, t)


def cmd_new(a):
    d = PROJECTS / a.name
    if d.exists():
        die(f"{d} already exists")
    shutil.copytree(PROJECTS / "_template", d)
    title = a.title or a.name.replace("-", " ").title()
    subs = {"{{title}}": title, "{{profile}}": a.profile}
    for f in ("CONTEXT.md", "LOG.md", "DECISIONS.md"):
        t = read(d / f)
        for k, v in subs.items():
            t = t.replace(k, v)
        write(d / f, t)
    t = read(d / "project.yaml")
    for k, v in {"name": a.name, "title": title, "profile": a.profile, "created_by": a.tool,
                 "created_at": today(), "updated_by": a.tool, "updated_at": today(),
                 "origin_tool": a.tool, "sync_to": fmt_list(parse_list(a.sync_to))}.items():
        t = set_field(t, k, v)
    t = add_history(t, today(), a.tool, "created")
    write(d / "project.yaml", t)
    append(d / "LOG.md", f"{now()} | {a.tool} | created | project created (profile: {a.profile})\n")
    print(f"created projects/{a.name}")


def cmd_log(a):
    d = project_dir(a.name)
    append(d / "LOG.md", f"{now()} | {a.tool} | update | {a.note}\n")
    touch(d, a.tool, "update")
    print("logged")


def cmd_decide(a):
    d = project_dir(a.name)
    append(d / "DECISIONS.md",
           f"\n## {today()} · {a.tool} · {a.what}\n- Decision: {a.what}\n- Why: {a.why}\n")
    append(d / "LOG.md", f"{now()} | {a.tool} | decision | {a.what}\n")
    touch(d, a.tool, "decision")
    print("decision recorded")


def files_of(d):
    return sorted(p for p in d.rglob("*") if p.is_file() and p.name not in SKIP)


def cmd_export(a):
    d = project_dir(a.name)
    rows = []
    for p in files_of(d):
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
        rows.append(f"| `{p.relative_to(d)}` | {p.stat().st_size} | {h} |")
    pt = read(d / "project.yaml")
    manifest = (f"# Manifest — {get_field(pt, 'title')}\n\n"
                f"Exported by **{a.tool}** on {now()}. Origin tool: {get_field(pt, 'origin_tool')}. "
                f"Profile: {get_field(pt, 'profile')}.\n\n"
                "A receiving agent should find every file below in this folder.\n\n"
                "| File | Bytes | sha256 (12) |\n|---|---|---|\n" + "\n".join(rows) + "\n")
    write(d / "MANIFEST.md", manifest)
    t = read(d / "project.yaml")
    t = set_field(t, "exported_by", a.tool)
    t = set_field(t, "exported_at", today())
    write(d / "project.yaml", t)
    append(d / "LOG.md", f"{now()} | {a.tool} | export | manifest written, {len(rows)} files\n")
    touch(d, a.tool, "export")
    missing = [f for f in ("CONTEXT.md", "DECISIONS.md", "LOG.md") if len(read(d / f).strip().splitlines()) < 3]
    if not any(x.name != ".gitkeep" for x in (d / "files").glob("*")):
        print("warning: files/ is empty - did you put the project's files there?")
    for f in missing:
        print(f"warning: {f} looks empty")
    print(f"exported {len(rows)} files. Now: git add -A && git commit -m '{a.tool} | {a.name} | export' && git push")


def cmd_import(a):
    d = project_dir(a.name)
    append(d / "LOG.md", f"{now()} | {a.tool} | import | project pulled and recreated in {a.tool}\n")
    touch(d, a.tool, "import")
    print(f"import recorded. Now: git add -A && git commit -m '{a.tool} | {a.name} | import' && git push")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    for n in ("new", "log", "decide", "export", "import"):
        s = sp.add_parser(n)
        s.add_argument("name")
        s.add_argument("--tool", required=True, help="claude | chatgpt | grok | ...")
        if n == "new":
            s.add_argument("--title")
            s.add_argument("--profile", default="none")
            s.add_argument("--sync-to", default="")
        if n == "log":
            s.add_argument("--note", required=True)
        if n == "decide":
            s.add_argument("--what", required=True)
            s.add_argument("--why", required=True)
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", a.name):
        die("project name: lowercase letters, digits, hyphens")
    {"new": cmd_new, "log": cmd_log, "decide": cmd_decide, "export": cmd_export, "import": cmd_import}[a.cmd](a)


if __name__ == "__main__":
    main()
