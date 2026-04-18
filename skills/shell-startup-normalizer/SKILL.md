---
name: shell-startup-normalizer
description: Use when Bash or Zsh startup files are messy, mixed together, shell-specific, or need to be actively reorganized into a cleaner split layout while preserving tool-managed blocks.
---

# Shell Startup Normalizer

## Overview

Normalize shell startup files by inspecting them first, classifying each block, preserving tool-managed content, creating backups, and rewriting into a thinner split layout.

This skill is for active migration work on files such as `.bashrc`, `.bash_profile`, `.profile`, `.zshrc`, `.zprofile`, `.zshenv`, `.bash_aliases`, and `.bash_functions`.

## When to Use

- Bash or Zsh startup logic is packed into one large file
- login setup, aliases, functions, PATH edits, and prompt setup are mixed together
- `.bashrc` or `.zshrc` contains repeated exports, stale comments, or copied snippets from multiple tools
- the user wants a portable shell layout that works across Linux Bash, Linux Zsh, and macOS Zsh
- startup files contain tool-managed blocks that must be preserved while the surrounding layout is cleaned up

Do not use this skill for a one-line alias change or when the user only wants explanation without edits.

## Inspection Order

Inspect before proposing edits.

For Bash, inspect in this order:
- `~/.bash_profile`
- `~/.profile`
- `~/.bashrc`
- `~/.bash_aliases`
- `~/.bash_functions`
- `~/.shell_env`, `~/.shell_aliases`, `~/.shell_functions`, `~/.shell_local` if they already exist

For Zsh, inspect in this order:
- `~/.zprofile`
- `~/.zshrc`
- `~/.zshenv`
- `~/.zlogin` if present
- `~/.shell_env`, `~/.shell_aliases`, `~/.shell_functions`, `~/.shell_local` if they already exist

## Classification

Classify every block before moving it:

- login bootstrap
- interactive shell setup
- environment variables
- PATH setup
- aliases
- functions
- prompt or theme setup
- completion setup
- tool-managed blocks
- machine-local config
- shell-specific config

Keep shell-specific syntax in shell-specific files. Do not move Bash-only syntax into shared files, and do not move Zsh-only syntax into shared files.

## Target Layout

Use this normalized layout unless the user asks for a different split:

- `~/.shell_env` for portable environment and PATH setup
- `~/.shell_aliases` for aliases only
- `~/.shell_functions` for reusable helper functions
- `~/.shell_local` for machine-local overrides
- `~/.bash_profile` for Bash login bootstrap
- `~/.bashrc` for Bash interactive setup
- `~/.zprofile` for Zsh login bootstrap
- `~/.zshrc` for Zsh interactive setup
- minimal `~/.zshenv` only when variables must exist for every Zsh invocation

Read [layout.md](references/layout.md) before rewriting file load order.

## Safety Rules

- create timestamped backups before editing any startup file
- preserve tool-managed blocks byte-for-byte when feasible
- keep prompt, plugin manager, and completion setup in interactive files
- use guarded sourcing for optional files
- preserve comments that express real local intent
- keep local override files late in load order
- never introduce output during non-interactive startup
- never silently drop unknown blocks

## Rewrite Workflow

1. Inspect all relevant startup files.
2. Summarize what each file currently does.
3. Classify each block and call out tool-managed sections explicitly.
4. Propose the target layout and any files that will be created.
5. Create backups.
6. Rewrite the main entry files into thin loaders.
7. Move aliases, functions, and portable env setup into the shared files where safe.
8. Preserve shell-specific and tool-managed content in the correct shell entry files.
9. Re-read the result for ordering mistakes and duplicate sourcing.

Read [migration-heuristics.md](references/migration-heuristics.md) when the current files are messy or ambiguous.

## Migration Summary

After editing, report:

- files backed up
- files created
- files modified
- aliases moved
- functions moved
- PATH or env setup consolidated
- tool-managed blocks preserved
- shell-specific content intentionally left in place
- manual follow-up items

Read [examples.md](references/examples.md) when the user wants a concrete before and after pattern.
