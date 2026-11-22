# End-of-day wrap-up (paste into any agent)

Read `AGENTS.md` in my ai-hub repo and follow it. Then wrap up this session:

1. For every project we touched: append to `projects/<name>/LOG.md` (who, when, what), add any decisions to `DECISIONS.md`,
   and refresh `CONTEXT.md` if facts changed. Put new files in `projects/<name>/files/`. Update `updated_by/updated_at` in `project.yaml`
   (use `python3 build/project.py log <name> --tool <you> --note "..."`).
2. If we changed a skill, bump it (`python3 build/skills.py bump ...`).
3. Record any new artifact, dashboard or automation in `registry/`.
4. Write `daily/<today>.md`: decisions, new facts, open items.
5. `python3 build/index.py`, then commit as `<tool> | <area> | <summary>` and push.
If you cannot push, give me the exact file contents to save.
