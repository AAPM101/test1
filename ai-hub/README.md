# ai-hub

One private repo that holds the owner's memory for every AI agent (Claude, ChatGPT, Grok, ...)
and every laptop (work, personal). Plain Markdown and YAML, synced with Git.

```
AGENTS.md          rules every agent follows (start here)
INDEX.md           auto-generated table of contents (python3 build/index.py)
me/                common to ALL agents and laptops: about, writing style, preferences
profiles/
  bsi/             BSI context (loaded only when a project says profile: bsi)
  personal/        personal context
skills/            one definition per skill, same name everywhere, with changelogs
projects/          one folder per project, with full provenance (who created/updated, what changed)
registry/          catalog of artifacts, dashboards, automations
daily/  inbox/     end-of-day notes and raw write-backs
build/             small stdlib-only Python scripts
prompts/           copy-paste prompts: wrap-up, morning, project export/import
```

## Setup on each laptop (once)
```bash
git clone <your-private-repo-url> ~/dev/ai-hub     # outside OneDrive/SharePoint
cd ~/dev/ai-hub/ai-hub                              # drop the extra level if the hub is its own repo
python3 build/index.py
```
Daily: `git pull` first, `git push` last. Tell any agent: "Read AGENTS.md in the hub and follow it."

## Scripts (Python 3, no dependencies)
| Command | What it does |
|---|---|
| `python3 build/project.py new <name> --tool claude --profile bsi --sync-to claude,chatgpt` | create a project from the template with provenance |
| `python3 build/project.py log <name> --tool chatgpt --note "..."` | append a LOG entry and update `updated_by/updated_at` |
| `python3 build/project.py decide <name> --tool claude --what "..." --why "..."` | add a decision |
| `python3 build/project.py export <name> --tool chatgpt` | write MANIFEST.md of all project files, mark exported |
| `python3 build/project.py import <name> --tool claude` | record that another agent pulled the project |
| `python3 build/skills.py new <name> --tool claude` / `bump <name> --tool grok --note "..."` | create / update a skill with changelog |
| `python3 build/index.py` | regenerate INDEX.md |
| `python3 build/context_pack.py [project]` | one file you can attach to an agent that can't use Git |

Privacy: keep the repo private, enable 2FA, never commit secrets or confidential BSI documents.
