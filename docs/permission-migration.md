# Permission Migration

How to replicate curated approval rules for Claude Code and Codex on a new machine.

API credentials and provider setup are handled separately by `install_cc_api.sh` and
`install_codex_api.sh` — those installers do not touch the permission files described here,
so there are no conflicts.

---

## Claude Code

Permissions live in the `permissions.allow` array in `~/.claude/settings.json`.
The template at `templates/claude/settings.json` contains the curated baseline.

Copy the `permissions` block into your `~/.claude/settings.json` on the new machine:

```json
"permissions": {
  "allow": [ ... ],
  "deny": []
}
```

Do not copy the `env` block — that is managed by `cc_api` and `install_cc_api.sh`.

**Format:** each entry is a glob prefix matched against the full command string.
`"Bash(git log *)"` allows any Bash command starting with `git log`.

---

## Codex

Rules live in `~/.codex/rules/default.rules`.
The template at `templates/codex/default.rules` contains the curated baseline.

Copy it directly — this file is standalone and does not interact with `config.toml`:

```bash
mkdir -p ~/.codex/rules
cp templates/codex/default.rules ~/.codex/rules/default.rules
```

`install_codex_api.sh` only merges provider sections into `config.toml` and never
touches the rules file, so running the installer after copying the rules is safe.

**Format:** each rule is a prefix matched against the argv array of the command.
`prefix_rule(pattern=["git", "log"], decision="allow")` allows `git log` and any
arguments that follow.

---

## Keeping the template up to date

New approvals accumulate in `~/.claude/settings.local.json` (Claude Code) and
`~/.codex/rules/default.rules` (Codex) as you work. Periodically review them,
promote any generally useful ones back into the templates in this repo, and commit.
