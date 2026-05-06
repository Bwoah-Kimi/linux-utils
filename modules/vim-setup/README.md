# vim-setup

Installable Claude Code skill for restoring a preferred Vim configuration, including Vundle, gruvbox, clipboard support, and editor defaults.

## Contents

```text
skill/SKILL.md              skill instructions
skill/claude/CLAUDE.md      Claude Code companion instructions
skill/references/*.md       prerequisites, plugin list, and vimrc baseline
install/*.sh                Claude Code installer
```

## Install

Canonical module installer:

```bash
bash modules/vim-setup/install/install_claude_vim_setup_skill.sh
```

Root compatibility wrapper:

```bash
bash install/install_claude_vim_setup_skill.sh
```

## What the installer does

- copies `skill/` to `~/.claude/skills/vim-setup`
- backs up an existing installed skill directory before replacing it
- does not mutate Vim config during installation

## Usage

After installing, ask Claude Code to set up Vim using the `vim-setup` skill.

The skill itself defines prerequisites, inspection steps, backup rules, and setup workflow in [`skill/SKILL.md`](skill/SKILL.md).
