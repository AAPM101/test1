#!/usr/bin/env python3
"""Regenerate INDEX.md: the first file every agent reads."""
from common import PROJECTS, ROOT, SKILLS, get_field, now, read, write
from skills import frontmatter_get


def main():
    out = [f"# INDEX\n\n_Generated {now()} by build/index.py. Read `AGENTS.md` first._\n",
           "## Always load\n- `me/about.md`\n- `me/writing-style.md`\n- `me/preferences.md`\n",
           "## Profiles (load only when a project names it)\n"]
    for d in sorted((ROOT / "profiles").iterdir()):
        if d.is_dir():
            out.append(f"- `profiles/{d.name}/profile.md`")
    out.append("\n## Skills\n| Skill | Version | Last updated by | Date |\n|---|---|---|---|")
    n = 0
    for d in sorted(SKILLS.iterdir()):
        f = d / "SKILL.md"
        if d.is_dir() and not d.name.startswith("_") and f.exists():
            t = read(f)
            out.append(f"| `{d.name}` | v{frontmatter_get(t, 'version')} | {frontmatter_get(t, 'updated_by')} | {frontmatter_get(t, 'updated_at')} |")
            n += 1
    if not n:
        out.append("| _none yet_ | | | |")
    out.append("\n## Projects\n| Project | Profile | Status | Created by | Last updated by | Date | Sync to |\n|---|---|---|---|---|---|---|")
    n = 0
    for d in sorted(PROJECTS.iterdir()):
        f = d / "project.yaml"
        if d.is_dir() and not d.name.startswith("_") and f.exists():
            t = read(f)
            g = lambda k: get_field(t, k) or ""
            out.append(f"| [{d.name}](projects/{d.name}/CONTEXT.md) | {g('profile')} | {g('status')} | {g('created_by')} | "
                       f"{g('updated_by')} | {g('updated_at')} | {g('sync_to')} |")
            n += 1
    if not n:
        out.append("| _none yet_ | | | | | | |")
    out.append("\n## Registries\n- `registry/artifacts.yaml`\n- `registry/dashboards.yaml`\n- `registry/automations.yaml`\n")
    write(ROOT / "INDEX.md", "\n".join(out) + "\n")
    print("INDEX.md written")


if __name__ == "__main__":
    main()
