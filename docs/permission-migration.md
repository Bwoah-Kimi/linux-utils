# Permission Migration

How to replicate curated approval rules for Claude Code and Codex on a new machine.

API credentials and provider setup are handled separately by `install_cc_api.sh` and
`install_codex_api.sh` — those installers do not touch the permission files described here,
so there are no conflicts.

---

## Approach: broad allow + targeted deny

Both Claude Code and Codex use the same model:

- **Allow broadly** at the tool level (Claude Code) or project level (Codex), so common
  development commands run without per-command prompts.
- **Deny destructive operations** explicitly, so accidents like `rm -rf`, `git reset --hard`,
  or `git push --force` are blocked even when broad allow is in effect.
- **Deny outranks allow.** A command matched by both lists is denied.

This is the inverse of the older "narrow allowlist + empty denylist" approach, which
prompted on every uncommon command. The deny list is best-effort — it catches typical
mistakes, not adversaries. Prefix matching is approximate, so `rm -rf` and `rm -fr` are
different rules and must each be listed.

---

## Claude Code

Permissions live in `permissions.allow` and `permissions.deny` arrays in
`~/.claude/settings.json`. The template at `modules/api-switcher/templates/claude/settings.json` contains the
curated baseline.

Copy the `permissions` block into your `~/.claude/settings.json` on the new machine:

```json
"permissions": {
  "allow": [
    "Bash",
    "Read",
    "Edit",
    "Write",
    "Glob",
    "Grep"
  ],
  "deny": [
    "Bash(rm -rf *)",
    "Bash(git push --force *)",
    "Bash(git reset --hard *)",
    ...
  ]
}
```

Do not copy the `env` block — that is managed by `cc_api` and `install_cc_api.sh`.

**Allow format:** a bare tool name like `"Bash"` allows the entire tool; a parenthesized
form like `"Bash(git log *)"` is a glob prefix matched against the full command string.

**Deny format:** same syntax. Prefix matching means flag-order matters —
`Bash(rm -rf *)` does not match `rm -fr ...`, so flag-permutation variants are listed
separately in the template.

---

## Codex

Codex's permission model is split across two files:

1. **`~/.codex/config.toml`** — per-project `trust_level = "trusted"` entries grant the
   broad-allow half of the model. Inside a trusted project root, Codex auto-approves
   commands without consulting the rules file. This is set per project, e.g.:

   ```toml
   [projects.'d:\dev-tools']
   trust_level = "trusted"
   ```

2. **`~/.codex/rules/default.rules`** — `prefix_rule` entries supply (a) explicit allow
   rules for common read-only commands so they pass outside trusted projects, and (b) a
   deny block for destructive operations.

The template at `modules/api-switcher/templates/codex/default.rules` contains the curated baseline. Copy it
directly — this file is standalone and does not interact with `config.toml`:

```bash
mkdir -p ~/.codex/rules
cp modules/api-switcher/templates/codex/default.rules ~/.codex/rules/default.rules
```

`install_codex_api.sh` only merges provider sections into `config.toml` and never
touches the rules file or `trust_level` entries, so running the installer after copying
the rules is safe. Trust levels for new projects are set manually the first time you
open them in Codex.

**Format:** each rule is a prefix matched against the argv array of the command.
`prefix_rule(pattern=["git", "log"], decision="allow")` allows `git log` and any
arguments that follow. `decision="deny"` blocks the matching prefix.

---

## What's denied

The destructive deny list is shared between both tools and covers:

- Filesystem destruction: `rm -rf` (and flag-order variants), `sudo rm`, `dd`, `mkfs`,
  `chmod -R 777`, `chown -R`
- Git destruction: `--force` push, `reset --hard`, `clean -f[dx]`, `checkout -- <path>`,
  `branch -D`
- System power: `shutdown`, `reboot`, `halt`, `poweroff`

Things the deny list does **not** reliably catch:

- `curl ... | sh` and similar pipe-to-shell patterns — pipes aren't part of the matched
  prefix
- Fork bombs — special characters break the parser
- `--force-push` to specific branches only — branch names aren't in the prefix
- Variants with extra whitespace, environment-variable-built paths, or escaped commands

Treat the deny list as guardrails for accidents, not adversaries. When something
legitimate is blocked, edit the deny list or approve once at the prompt.

---

## Keeping the template up to date

New approvals accumulate in `~/.claude/settings.local.json` (Claude Code) and
`~/.codex/rules/default.rules` (Codex) as you work. Periodically review them, promote
any generally useful ones back into the modules/api-switcher/templates in this repo, and commit.
