# Linux Utils Helper Packaging Design

**Date:** 2026-04-16

## Goal

Package the existing local helper scripts and their helper-managed configuration into the `linux-utils` repository so they can be installed on a new Linux machine by cloning the repo and running installer scripts.

The initial scope covers:

- `codex_api`
- `cc_api`
- `proxy`

Future scope can include additional dotfiles and Linux environment customizations such as Vim configuration.

## Context

The current helpers already exist in the local machine under `~/.local/bin` and depend on local files under `~/.codex`, `~/.claude`, and shell startup files. They are useful, but they are not yet portable:

- the scripts are not stored in a managed repository
- related config files are mixed with machine-local state
- some dependent files contain real secrets and cannot be committed as-is
- there is no install workflow for a new machine

The new repository should become the source of truth for portable helper logic and helper-owned template files, while preserving machine-specific local state where appropriate.

## Non-Goals

This phase does not aim to:

- manage every local config file under `~/.codex` or `~/.claude`
- commit real API keys or private tokens
- introduce symlink-based dotfile management
- build a full generic dotfile manager
- migrate future tools such as Vim in the same implementation batch

## Recommended Repo Layout

Use a simple copy-based structure with per-helper installers and shared install utilities.

```text
linux-utils/
  bin/
    codex_api
    cc_api
    proxy
  install/
    install_codex_api.sh
    install_cc_api.sh
    install_proxy.sh
  lib/
    install_common.sh
    merge_codex_config.py
  templates/
    codex/
      auth_list.json
      config.providers.toml
    claude/
      provider_list.json
  docs/
    superpowers/
      specs/
        2026-04-16-linux-utils-helper-packaging-design.md
  README.md
```

## Installation Model

The repository installs files by copying them into the user’s home directory, not by creating symlinks.

This choice is intentional:

- it works cleanly on machines where the repo may later be moved or deleted
- it makes the installed state explicit
- it avoids requiring the repo to remain in a fixed filesystem location
- it matches the user preference to copy into place rather than link

Installers should create target directories as needed where safe, set executable bits for scripts, and make timestamped backups before replacing managed files.

## Helper Packaging Rules

### `codex_api`

Repository-owned files:

- `bin/codex_api`
- `templates/codex/auth_list.json`
- `templates/codex/config.providers.toml`

Install behavior:

- copy `bin/codex_api` to `~/.local/bin/codex_api`
- require `~/.codex/` to already exist
- install `templates/codex/auth_list.json` to `~/.codex/auth_list.json`
- merge helper-managed provider configuration into `~/.codex/config.toml`

Helper-managed Codex config scope for this phase:

- top-level `model_provider`
- `[model_providers.*]`

Everything else in local `~/.codex/config.toml` must be preserved, including items such as:

- project trust sections
- notice settings
- model migrations
- user preferences unrelated to the helpers

The repository should not commit a full copy of a machine-local `config.toml`. Instead, it should commit a provider-only template file that the installer merges into the local config.

### `cc_api`

Repository-owned files:

- `bin/cc_api`
- `templates/claude/provider_list.json`

Install behavior:

- copy `bin/cc_api` to `~/.local/bin/cc_api`
- require `~/.claude/` to already exist
- install `templates/claude/provider_list.json` to `~/.claude/provider_list.json`

Local `~/.claude/settings.json` remains machine-local and is not replaced by the installer. The `cc_api` helper itself continues to manage only the provider-managed subset of `settings.json.env`.

### `proxy`

Repository-owned files:

- `bin/proxy`

Install behavior:

- copy `bin/proxy` to `~/.local/bin/proxy`
- update `~/.bash_functions` by inserting or replacing a clearly marked managed block containing the thin `proxy()` wrapper
- do not overwrite unrelated shell functions or other custom shell logic

The installer should assume `.bashrc` sources `~/.bash_functions`. If that assumption is false, the installer should warn clearly rather than silently editing `.bashrc`.

## Sanitized Template Rules

No real secrets may be committed to the repository.

Required sanitization rules:

- `templates/codex/auth_list.json` contains provider names with placeholder values such as `"<fill-me>"`
- `templates/claude/provider_list.json` contains placeholder tokens and placeholder URLs where applicable
- committed helper scripts must not embed real secrets
- existing local files with real secrets must be sanitized before being copied into the repo

The intended first-run workflow on a new machine is:

1. clone the repository
2. run one or more installer scripts
3. manually edit installed local files to insert real secrets

For the initial scope, the main manual secret entry points are:

- `~/.codex/auth_list.json`
- `~/.claude/provider_list.json`

## Installer Responsibilities

Each installer should:

- fail fast with clear errors if required base directories do not exist
- create `~/.local/bin` if missing
- copy the relevant executable into place
- set executable permissions
- make timestamped backups before replacing managed targets
- print a clear summary of what changed
- print any required manual follow-up steps

Shared behavior should live in a reusable shell library under `lib/`.

## Merge Strategy for Codex Config

Codex config merge behavior is the main place where install logic is not a simple copy.

Recommended approach:

- store helper-managed provider config in `templates/codex/config.providers.toml`
- use a small merge utility, likely Python-based, to:
  - parse the local `~/.codex/config.toml`
  - parse the provider template file
  - replace only the helper-managed keys
  - preserve all other local config

This avoids brittle text replacement while keeping ownership boundaries explicit.

## README Expectations

The top-level `README.md` should document:

- the repository purpose
- the directory layout
- quick install examples
- prerequisites for each installer
- which files are copied
- which files must be edited manually after install
- the fact that secrets are intentionally not stored in git

## Definition of Done

This phase is complete when:

- the repository contains portable copies of `codex_api`, `cc_api`, and `proxy`
- the repository contains sanitized template files with no real secrets
- the repository contains installer scripts for these helpers
- `install_codex_api.sh` can install `codex_api`, copy `auth_list.json`, and merge helper-managed Codex config into an existing `~/.codex/config.toml`
- `install_cc_api.sh` can install `cc_api` and copy `provider_list.json` into an existing `~/.claude/`
- `install_proxy.sh` can install `proxy` and update `~/.bash_functions` with the managed wrapper block
- the installed files are local copies, not symlinks
- a fresh machine with existing `~/.codex/` and `~/.claude/` can clone the repo and run the installer scripts to obtain working helper installations after manual secret entry

## Follow-On Work

Later phases can extend this repository with:

- Vim configuration
- additional shell helpers
- an optional `install_all.sh`
- more helper-managed Codex sections if desired
- other portable Linux environment customizations
