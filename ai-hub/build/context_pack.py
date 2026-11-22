#!/usr/bin/env python3
"""Build one file to attach to an agent that cannot use Git.

  context_pack.py                 -> me/ only (stdout)
  context_pack.py <project>       -> me/ + the project's profile + the project (CONTEXT, DECISIONS, LOG tail, MANIFEST)
Redirect to a file:  python3 build/context_pack.py my-project > pack.md
"""
import sys

from common import PROJECTS, ROOT, get_field, project_dir, read


def section(title, path):
    return f"\n\n=== {title} ({path.relative_to(ROOT)}) ===\n\n" + read(path) if path.exists() else ""


def main():
    parts = ["# Context pack. Follow AGENTS.md rules: identify yourself, record changes in LOG.md."]
    parts.append(read(ROOT / "AGENTS.md"))
    for f in ("about", "writing-style", "preferences"):
        parts.append(section(f"ME: {f}", ROOT / "me" / f"{f}.md"))
    if len(sys.argv) > 1:
        d = project_dir(sys.argv[1])
        pt = read(d / "project.yaml")
        prof = get_field(pt, "profile")
        if prof and prof != "none":
            parts.append(section(f"PROFILE: {prof}", ROOT / "profiles" / prof / "profile.md"))
        parts.append(section("PROJECT: project.yaml", d / "project.yaml"))
        for f in ("CONTEXT.md", "DECISIONS.md", "MANIFEST.md"):
            parts.append(section(f"PROJECT: {f}", d / f))
        log = (d / "LOG.md")
        if log.exists():
            parts.append("\n\n=== PROJECT: LOG (last 40 lines) ===\n\n" + "\n".join(read(log).splitlines()[-40:]))
    print("\n".join(parts))


if __name__ == "__main__":
    main()
