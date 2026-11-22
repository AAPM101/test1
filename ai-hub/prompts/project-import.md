# Pull a project from the hub (paste into the RECEIVING agent)

Read `AGENTS.md` in my ai-hub repo. `git pull`, then import the project "<NAME>":

1. Read `projects/<NAME>/project.yaml`, `CONTEXT.md`, `DECISIONS.md`, the tail of `LOG.md`, and `MANIFEST.md`.
2. Load `me/` and only the profile named in `project.yaml`.
3. Recreate the project in this tool (project instructions, context, files) from that material.
4. Run `python3 build/project.py import <NAME> --tool <this-tool>`, commit as `<tool> | <NAME> | import`, and push.
Tell me what you recreated and what could not be carried over.
