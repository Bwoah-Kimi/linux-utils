---
name: vim-setup
description: Use when setting up Vim on a new machine or restoring a preferred Vim configuration including Vundle, gruvbox, clipboard integration, and editor defaults.
---

# Vim Setup

## Overview

Set up Vim on a fresh or existing machine by inspecting the current state, installing prerequisites, bootstrapping Vundle, writing the baseline `.vimrc`, installing plugins, and verifying the result.

This skill is for provisioning or restoring a consistent Vim environment across machines.

## When to Use

- Setting up Vim on a new machine or fresh OS install
- The current `.vimrc` is missing, broken, or does not match the baseline
- Vundle or plugins are not installed
- Vim lacks clipboard support and needs the correct package
- The user asks to restore or replicate their Vim config

Do not use this skill for one-off vimrc tweaks or plugin experimentation.

## Inspection

Inspect before making changes:

1. Check Vim version and clipboard support: `vim --version | grep clipboard`
2. Read `~/.vimrc` if it exists
3. List `~/.vim/bundle/` if it exists
4. Check whether `~/.gvimrc` exists
5. Check whether `git` is available

## Prerequisites

Read [prerequisites.md](references/prerequisites.md) to determine which system packages are needed and how to verify them.

## Workflow

1. Inspect the current Vim setup as described above.
2. Report findings to the user before making changes.
3. Check prerequisites and prompt the user to install any missing packages.
4. Create a timestamped backup of `~/.vimrc` if it exists.
5. Create a timestamped backup of `~/.vim/` if it exists and will be modified.
6. Write or merge the baseline `.vimrc` from [vimrc-baseline.md](references/vimrc-baseline.md).
7. Bootstrap Vundle if `~/.vim/bundle/Vundle.vim` is missing.
8. Run `:PluginInstall` to install declared plugins.
9. Verify: recheck clipboard support, confirm gruvbox loads, confirm plugins are present.

Read [plugins.md](references/plugins.md) for the full plugin list and declarations.

## Safety Rules

- Create timestamped backups before editing `~/.vimrc` or `~/.vim/`
- Preserve user customizations that are not part of the baseline
- Do not delete existing plugins that the user may have added
- Do not overwrite `~/.vimrc` without showing the user what will change
- If Vundle is already bootstrapped, do not re-clone it
- Prompt the user for package installation rather than running it silently

## Setup Summary

After completing setup, report:

- Vim version and clipboard support status
- Packages that were or need to be installed
- Files backed up (with paths)
- Whether `.vimrc` was created or updated
- Whether Vundle was bootstrapped
- Plugins installed via `:PluginInstall`
- Any manual follow-up items
