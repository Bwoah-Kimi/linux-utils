# shell-startup-normalizer

Installable Codex and Claude Code skill for reorganizing messy Bash/Zsh startup files while preserving tool-managed blocks.

## Contents

```text
skill/SKILL.md              Codex-compatible skill instructions
skill/claude/CLAUDE.md      Claude Code companion instructions
skill/references/*.md       layout, migration, and example references
install/*.sh                Codex and Claude Code installers
```

## Install

Canonical module installers:

```bash
bash modules/shell-startup-normalizer/install/install_codex_shell_startup_skill.sh
bash modules/shell-startup-normalizer/install/install_claude_shell_startup_skill.sh
```

Root compatibility wrappers:

```bash
bash install/install_codex_shell_startup_skill.sh
bash install/install_claude_shell_startup_skill.sh
```

## What the installers do

- copy `skill/` to `~/.codex/skills/shell-startup-normalizer` or `~/.claude/skills/shell-startup-normalizer`
- back up an existing installed skill directory before replacing it
- do not mutate shell startup files

## Usage

After installing, ask Codex or Claude Code to normalize messy shell startup files using the `shell-startup-normalizer` skill.

The skill itself defines the inspection order, target layout, safety rules, and migration heuristics in [`skill/SKILL.md`](skill/SKILL.md).
