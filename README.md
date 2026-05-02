# linux-utils

Portable scripts, helper installers, and agent skills for Linux and Windows environments.

## Current Helpers

- `cc_api` — switch Claude Code API providers
- `codex_api` — switch Codex API providers
- `proxy` — manage HTTP/HTTPS/SOCKS5 proxy env vars
- `shell-startup-normalizer` skill for Codex and Claude Code
- `vim-setup` skill for Claude Code

These helpers live in the repo and are installed by copying files into your home directory. They are not symlinked back to the repository.

## Repo Layout

```text
bin/        portable helper executables (Linux/WSL shebang scripts + Windows .bat launchers)
docs/       guides and reference docs
install/    per-helper install scripts (bash for Linux/WSL, PowerShell for Windows)
lib/        shared installer and merge utilities
skills/     portable agent skills and references
templates/  sanitized helper-owned config templates
tests/      repo-local verification scripts
```

## Prerequisites

**Linux / WSL**
- `~/.codex/` must already exist before running `install_codex_api.sh`
- `~/.claude/` must already exist before running `install_cc_api.sh`
- `~/.bashrc` should source `~/.bash_functions` for the `proxy` wrapper to be active
- `python3` must be available
- `curl` should be available for live `proxy status` output

**Windows (native)**
- `%USERPROFILE%\.codex\` must already exist before running `install_codex_api_windows.ps1`
- `%USERPROFILE%\.claude\` must already exist before running `install_cc_api_windows.ps1`
- `python` must be available on `PATH`

## Install

Clone the repo and run only the installers you want.

**Linux / WSL**

```bash
git clone <your-repo-url> linux-utils
cd linux-utils

bash install/install_codex_api.sh
bash install/install_cc_api.sh
bash install/install_proxy.sh
bash install/install_codex_shell_startup_skill.sh
bash install/install_claude_shell_startup_skill.sh
bash install/install_claude_vim_setup_skill.sh
```

**Windows (native PowerShell)**

```powershell
git clone <your-repo-url> linux-utils
cd linux-utils

.\install\install_codex_api_windows.ps1
.\install\install_cc_api_windows.ps1
```

The Windows installers copy both the Python script and a `.bat` launcher to
`%USERPROFILE%\.local\bin\`. Add that directory to your `PATH` if it is not already there.

## What Each Installer Does

### `install/install_cc_api.sh` / `install_cc_api_windows.ps1`

- copies `bin/cc_api` to `~/.local/bin/cc_api` (and `cc_api.bat` on Windows)
- merges `templates/claude/provider_list.json` into `~/.claude/provider_list.json`
  — existing provider entries and their tokens are preserved; new template entries are added with placeholder values
- leaves `~/.claude/settings.json` untouched

### `install/install_codex_api.sh` / `install_codex_api_windows.ps1`

- copies `bin/codex_api` to `~/.local/bin/codex_api` (and `codex_api.bat` on Windows)
- merges `templates/codex/auth_list.json` into `~/.codex/auth_list.json`
  — existing API keys are preserved; new template entries are added with placeholder values
- merges helper-managed provider config into `~/.codex/config.toml`
  — preserves unrelated local Codex config such as project trust settings

### `install/install_proxy.sh`

- copies `bin/proxy` to `~/.local/bin/proxy`
- inserts or updates a managed `proxy()` wrapper block in `~/.bash_functions`
- preserves unrelated shell functions

### `install/install_codex_shell_startup_skill.sh`

- copies `skills/shell-startup-normalizer` to `~/.codex/skills/shell-startup-normalizer`
- backs up an existing installed skill directory before replacing it

### `install/install_claude_shell_startup_skill.sh`

- copies `skills/shell-startup-normalizer` to `~/.claude/skills/shell-startup-normalizer`
- backs up an existing installed skill directory before replacing it

### `install/install_claude_vim_setup_skill.sh`

- copies `skills/vim-setup` to `~/.claude/skills/vim-setup`
- backs up an existing installed skill directory before replacing it

None of the skill installers mutate shell startup files or editor config.

## Helper Usage

### `cc_api`

```bash
cc_api -l, --list              # list available Claude Code providers
cc_api -c, --current           # show active provider
cc_api -s, --switch <provider> # switch to a provider
```

### `codex_api`

```bash
codex_api -l, --list              # list available Codex providers
codex_api -c, --current           # show active provider
codex_api -s, --switch <provider> # switch to a provider
```

## Manual Follow-Up

The repo intentionally does not store real API keys or private tokens.

After a first-time installation, fill in real secrets in:

- `~/.codex/auth_list.json` — one key per Codex provider alias
- `~/.claude/provider_list.json` — env vars per Claude Code provider

Re-running an installer after adding new providers to the templates will add the
new entries without touching your existing keys.

If multiple Codex provider aliases share the same upstream API key, repeat that
key under each alias in `~/.codex/auth_list.json`.

## Permission Migration

Curated approval rules for Claude Code and Codex are stored in:

- `templates/claude/settings.json` — Claude Code `permissions.allow` entries
- `templates/codex/default.rules` — Codex `prefix_rule` entries

See [`docs/permission-migration.md`](docs/permission-migration.md) for how to
apply these to a new machine without overwriting credentials.

## Verification

```bash
python3 -m pytest tests/ -v
```

## Notes

- Template files contain sanitized placeholders only — no real keys
- JSON installers merge rather than replace: existing values are always preserved
- Codex config installation merges only `[model_providers.*]` sections, leaving everything else intact
- Skill installers copy guidance files only; they do not edit shell or editor config
