# Push a project to the hub (paste into the ORIGINATING agent)

Read `AGENTS.md` in my ai-hub repo. Export the project "<NAME>" from this tool to `projects/<NAME>/`:

- `project.yaml`: created_by/origin_tool = this tool, profile = <bsi|personal|none>, sync_to = [<tools>]
- `CONTEXT.md`: goal, status, key facts, current state, open items, and the instructions you were following
- `DECISIONS.md`: every decision, with why, who, when
- `LOG.md`: a chronological history of what was done and which tool did it (reconstruct as best you can; mark reconstructed lines)
- `files/`: every file, document, dataset, prompt and artifact source you hold for this project
- `lanes/<this-tool>.md`: tool-specific notes and quirks
Then run `python3 build/project.py export <NAME> --tool <this-tool>`, commit as `<tool> | <NAME> | export`, and push.
List anything you could not export (e.g. chat history you cannot read).
