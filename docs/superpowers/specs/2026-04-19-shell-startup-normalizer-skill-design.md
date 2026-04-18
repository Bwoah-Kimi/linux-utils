# Shell Startup Normalizer Skill Design

**Date:** 2026-04-19

## Goal

Create a reusable skill that can actively formalize messy Bash and Zsh startup files into a clear, portable shell initialization layout.

The skill should work for Linux Bash, Linux Zsh, and macOS Zsh. It should be stored in `linux-utils` as the canonical source and installable for both Codex and Claude Code.

## Context

Current shell startup files often become messy because many concerns are mixed together:

- aliases
- shell functions
- PATH and environment setup
- prompt/theme setup
- tool-managed blocks such as Conda, oh-my-posh, Homebrew, plugin managers
- machine-specific overrides

The current machine already uses a better split than many default systems:

- `.bashrc` stays mostly as the interactive entrypoint
- `.bash_aliases` stores aliases
- `.bash_functions` stores functions and environment helper functions
- Conda and oh-my-posh are tolerated as tool-managed blocks

Other machines, including macOS machines using Zsh, may not have this structure. The skill should help Codex or Claude Code inspect existing startup files, preserve intent, and actively rewrite them into a cleaner split layout.

## Non-Goals

This skill should not:

- delete startup files without backups
- remove tool-managed blocks just because they look noisy
- force Bash and Zsh into identical syntax
- manage every possible shell framework or plugin manager
- replace a full dotfile manager
- silently edit files without first understanding and summarizing what will change

## Good Practices For Shell Startup Files

The skill should encode these principles:

- Keep main entry files thin.
- Separate concerns by file.
- Distinguish login shell setup from interactive shell setup.
- Centralize PATH and environment mutations.
- Keep aliases out of rc entrypoints.
- Keep reusable functions out of rc entrypoints.
- Preserve tool-managed blocks.
- Preserve machine-local escape hatches.
- Use clear managed block markers when a tool owns a section.
- Prefer idempotent PATH helpers over repeated `export PATH=...:$PATH` snippets.
- Keep shell-specific syntax in shell-specific files.

## Target Layout

### Shared Cross-Shell Files

`~/.shell_env`

- portable environment variables
- portable PATH helper functions
- PATH setup shared by Bash and Zsh
- safe to source from login startup files

`~/.shell_aliases`

- aliases only
- avoid shell-specific features unless guarded

`~/.shell_functions`

- shell-agnostic helper functions where possible
- small wrappers around repo-installed scripts

`~/.shell_local`

- machine-local overrides
- secrets-free but host-specific config
- not assumed to be portable

### Bash Files

`~/.bash_profile`

- login-shell bootstrap
- source `~/.profile` when appropriate
- source `~/.shell_env`
- source `~/.bashrc` for interactive shells when needed

`~/.bashrc`

- interactive guard near the top
- source `~/.shell_env`
- source `~/.shell_aliases`
- source `~/.shell_functions`
- optionally source legacy `~/.bash_aliases` and `~/.bash_functions` during migration
- preserve tool-managed interactive blocks such as Conda and oh-my-posh
- source `~/.shell_local` and `~/.bash_local` if present

### Zsh Files

`~/.zprofile`

- login-shell bootstrap
- source `~/.shell_env`
- keep macOS-specific login setup here when appropriate

`~/.zshrc`

- interactive shell setup
- source `~/.shell_env`
- source `~/.shell_aliases`
- source `~/.shell_functions`
- preserve plugin managers, prompt/theme setup, and tool-managed blocks
- source `~/.shell_local` and `~/.zsh_local` if present

`~/.zshenv`

- keep minimal
- avoid output, prompts, aliases, and expensive commands
- use only when variables must exist for every zsh invocation

## Skill Packaging

Canonical source lives in this repo:

```text
skills/
  shell-startup-normalizer/
    SKILL.md
    references/
      layout.md
      migration-heuristics.md
      examples.md
```

Codex install target:

```text
~/.codex/skills/shell-startup-normalizer/
```

Claude Code install target:

For the first iteration, install a Claude-facing companion playbook generated from the same canonical guidance instead of building a full plugin.

Recommended location:

```text
~/.claude/skills/shell-startup-normalizer/
```

If Claude Code later requires plugin-native packaging for better discovery, the canonical skill can be adapted into a plugin without changing the underlying guidance.

## Installer Scripts

Add repo installers:

```text
install/install_codex_shell_startup_skill.sh
install/install_claude_shell_startup_skill.sh
```

Install behavior:

- copy the canonical skill folder into the tool-specific target
- create parent directories if needed
- replace an existing installed copy only after backing it up
- print install location and trigger phrase
- never mutate user shell startup files during skill installation

## Skill Workflow

When the skill is used, the agent should:

1. Inspect relevant files.
2. Classify content blocks.
3. Identify tool-managed blocks.
4. Propose a target layout.
5. Back up files before editing.
6. Rewrite into the normalized layout.
7. Print a migration summary.
8. Suggest shell reload and smoke checks.

Relevant files to inspect:

- Bash: `.bashrc`, `.bash_profile`, `.profile`, `.bash_aliases`, `.bash_functions`
- Zsh: `.zshrc`, `.zprofile`, `.zshenv`, `.zlogin`
- shared files if present: `.shell_env`, `.shell_aliases`, `.shell_functions`, `.shell_local`

Content classifications:

- login bootstrap
- interactive shell setup
- environment variables
- PATH setup
- aliases
- functions
- prompt/theme setup
- completion setup
- tool-managed blocks
- machine-local config
- shell-specific config

## Tool-Managed Block Rules

The skill should preserve known generated blocks and avoid rewriting their internals unless asked.

Examples:

- Conda `conda initialize`
- oh-my-posh initialization
- Homebrew `shellenv`
- zinit, antidote, oh-my-zsh, starship, powerlevel10k
- language manager init blocks such as pyenv, rbenv, nvm, fnm, direnv

The skill may move a tool-managed block to a more appropriate entry file only after explaining why and preserving it byte-for-byte when feasible.

## Rewrite Rules

The skill should:

- preserve file permissions where practical
- create timestamped backups before editing
- avoid moving Bash-only syntax into shared files
- avoid moving Zsh-only syntax into shared files
- preserve comments that explain real local intent
- replace noisy boilerplate comments with short section headers
- use managed block markers for generated wrapper functions
- keep local overrides at the end of the load order

The skill should not:

- remove unknown blocks without asking
- source files that do not exist without guards
- create output during non-interactive startup
- put aliases or prompts in login-only files
- put slow network commands in startup files

## Migration Summary

After rewriting, the agent should report:

- files backed up
- files created
- files modified
- aliases moved
- functions moved
- PATH/env changes consolidated
- tool-managed blocks preserved
- shell-specific content left in Bash or Zsh files
- items requiring manual review

## Cross-Tool Behavior

Codex should use the skill as a normal local skill through `SKILL.md`.

Claude Code should receive the same workflow through an installed companion directory. The first iteration can be a readable playbook rather than a native Claude plugin, as long as Claude Code can be pointed to it and use the same normalization workflow.

## Definition Of Done

The implementation is complete when:

- `linux-utils` contains the canonical skill folder
- the skill has concise trigger metadata and actionable workflow guidance
- reference files cover layout, migration heuristics, and examples
- Codex installer copies the skill into `~/.codex/skills/shell-startup-normalizer/`
- Claude installer copies the companion into `~/.claude/skills/shell-startup-normalizer/`
- tests verify the skill files and installers exist and copy into temporary homes
- README documents how to install the skill for Codex and Claude Code

## Follow-On Work

Potential later improvements:

- a deterministic migration script for simple cases
- a Claude Code plugin wrapper if the companion playbook is not discoverable enough
- integration with future `linux-utils` dotfile installers
- templates for `.bashrc`, `.zshrc`, `.shell_env`, `.shell_aliases`, and `.shell_functions`
