# AGENTS.md — rules for every AI agent using this hub

This file applies to **every** agent (Claude, ChatGPT, Grok, any other) on **every** laptop.
If you are an agent, follow it exactly. The owner decides what syncs; you never assume.

## 1. Start of every session
1. `git pull` (or confirm you have the latest copy).
2. Read `INDEX.md`.
3. Always load `me/` (about, writing style, preferences). These are common to all agents.
4. Load a profile **only** if the work needs it:
   - Project work: the profile named in `projects/<name>/project.yaml` (`profile:`).
   - `profile: none` means the work is unrelated to any employer: ignore all of `profiles/`.
   - Never read a profile the task does not name.
5. Load only the skills you need from `skills/` (see `skills/registry.yaml`).

## 2. Identify yourself
Every write carries your tool name: `claude`, `chatgpt`, `grok`, or another lowercase name.
Use the same name every time, with the laptop in brackets if known, e.g. `claude[work-laptop]`.

## 3. Projects (the owner decides what syncs)
- Everything about a project lives in `projects/<name>/`. See `projects/_template/`.
- Provenance is mandatory and lives in `projects/<name>/project.yaml`:
  `created_by`, `created_at`, `updated_by`, `updated_at`, and a `history` of syncs.
- Every change is appended to `projects/<name>/LOG.md` (who, when, what). Never rewrite old lines.
- Decisions go in `DECISIONS.md` (what, why, who, when).
- `CONTEXT.md` is the one-page current truth. Overwrite it when facts change; keep it short.
- Deliverables and source material go in `projects/<name>/files/`.
- Your own scratch notes go in `projects/<name>/lanes/<your-tool>.md`. Edit only your own lane.

### Pushing a project to the hub ("export")
When the owner says "push project X to the repo", you (the originating agent):
1. Write/refresh `CONTEXT.md`, `DECISIONS.md`, `LOG.md`, your lane file, and put every file you hold for the project in `files/`.
2. Fill `project.yaml` (including `profile`, `sync_to`).
3. Run `python3 build/project.py export <name> --tool <you>` (or do the same steps by hand). It writes `MANIFEST.md` listing every file.
4. Commit and push: `<tool> | <name> | export: <summary>`.
If you cannot run scripts, create the same files by hand and tell the owner what is missing.

### Pulling a project from the hub ("import")
When the owner says "sync project X":
1. `git pull`, then read `projects/<name>/project.yaml`, `CONTEXT.md`, `DECISIONS.md`, the tail of `LOG.md`, and `MANIFEST.md`.
2. Recreate the project in your own tool from that material (instructions, context, files).
3. Run `python3 build/project.py import <name> --tool <you>` to record the sync in `project.yaml` and `LOG.md`.
4. Commit and push: `<tool> | <name> | import: <summary>`.
Anything your tool cannot hold (e.g. old chat history) will not be in the repo; say so rather than guess.

## 3. Skills
- One definition per skill: `skills/<name>/SKILL.md`. The name is identical in every tool.
- To change a skill: edit `SKILL.md`, bump `version` in its frontmatter, add a line to that skill's `CHANGELOG.md`
  (`date | tool | change | version`), update `skills/registry.yaml`
  (or run `python3 build/skills.py bump <name> --tool <you> --note "..."`).
- Commit: `<tool> | skill:<name> | <what changed>`.
- Other agents pick up the latest version when they pull. Refresh on demand or weekly.

## 4. Commits and safety
- Commit message format: `<tool> | <project or skill or area> | <what changed>`.
- Never delete another tool's lane file or rewrite history.
- Never store secrets, passwords, API keys or customer data in this repo.
- BSI content belongs in `profiles/bsi/` only. Keep it high level; do not paste confidential BSI documents or data.
- If two agents edited the same file, keep both changes and note the conflict in `LOG.md`; do not silently overwrite.

## 5. End of every session
Run the wrap-up in `prompts/wrap-up.md`: update LOG/CONTEXT/DECISIONS for touched projects, write `daily/<date>.md`
if useful, run `python3 build/index.py`, commit and push.
