# Profiles

One folder per context. `me/` is always loaded; a profile is loaded only when a project names it.

- `bsi/` — BSI work
- `personal/` — personal projects
- New employer: copy `bsi/` to `<employer>/` and edit. Point new projects at it with `profile: <employer>`.
- Work unrelated to any employer: set `profile: none` in the project; agents ignore all of `profiles/`.

This is an instruction agents follow, not an access lock. For real isolation from a specific agent, keep that
content out of the repo that agent can reach.
