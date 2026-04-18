# linux-utils

Portable scripts and helper installers for a Linux environment.

## Current Helpers

- `codex_api`
- `cc_api`
- `proxy`
- `shell-startup-normalizer` skill for Codex and Claude Code

These helpers live in the repo and are installed by copying files into your home directory. They are not symlinked back to the repository.

## Repo Layout

```text
bin/        portable helper executables
install/    per-helper install scripts
lib/        shared installer and merge utilities
skills/     portable agent skills and references
templates/  sanitized helper-owned config templates
tests/      repo-local verification scripts
```

## Prerequisites

- `~/.codex/` must already exist before running `install_codex_api.sh`
- `~/.claude/` must already exist before running `install_cc_api.sh`
- `~/.bashrc` should source `~/.bash_functions` for the `proxy` wrapper to be active in new shells
- `python3` must be available
- `curl` should be available for live `proxy status` output

## Install

Clone the repo and run only the installers you want:

```bash
git clone <your-repo-url> linux-utils
cd linux-utils

bash install/install_codex_api.sh
bash install/install_cc_api.sh
bash install/install_proxy.sh
bash install/install_codex_shell_startup_skill.sh
bash install/install_claude_shell_startup_skill.sh
```

## What Each Installer Does

### `install/install_codex_api.sh`

- copies `bin/codex_api` to `~/.local/bin/codex_api`
- copies `templates/codex/auth_list.json` to `~/.codex/auth_list.json`
- merges helper-managed provider config into `~/.codex/config.toml`
- preserves unrelated local Codex config such as project trust settings

### `install/install_cc_api.sh`

- copies `bin/cc_api` to `~/.local/bin/cc_api`
- copies `templates/claude/provider_list.json` to `~/.claude/provider_list.json`
- leaves `~/.claude/settings.json` untouched

### `install/install_proxy.sh`

- copies `bin/proxy` to `~/.local/bin/proxy`
- inserts or updates a managed `proxy()` wrapper block in `~/.bash_functions`
- preserves unrelated shell functions

### `install/install_codex_shell_startup_skill.sh`

- copies `skills/shell-startup-normalizer` to `~/.codex/skills/shell-startup-normalizer`
- backs up an existing installed skill directory before replacing it
- does not mutate `.bashrc`, `.zshrc`, or any other shell startup file

### `install/install_claude_shell_startup_skill.sh`

- copies `skills/shell-startup-normalizer` to `~/.claude/skills/shell-startup-normalizer`
- includes the Claude-facing companion playbook at `claude/CLAUDE.md`
- backs up an existing installed skill directory before replacing it
- does not mutate `.bashrc`, `.zshrc`, or any other shell startup file

## Shell Startup Skill Usage

The canonical skill lives at `skills/shell-startup-normalizer/` in this repo. After installation, ask Codex or Claude Code to use the shell-startup-normalizer skill when you want it to inspect messy Bash or Zsh startup files, preserve tool-managed blocks, create backups, and reorganize the files into a cleaner split layout.

The skill installers only install guidance files. They do not change your shell startup files by themselves.

## Manual Follow-Up

The repo intentionally does not store real API keys or private tokens.

After installation, fill in real secrets in:

- `~/.codex/auth_list.json`
- `~/.claude/provider_list.json`

If multiple Codex provider aliases share the same upstream API key, repeat that same key under each alias in `~/.codex/auth_list.json`.

Then reload your shell if needed:

```bash
source ~/.bash_functions
```

or open a new shell session.

## Verification

Repo-local verification scripts live under `tests/`. The main full pass is:

```bash
python3 tests/test_templates_sanitized.py
python3 tests/test_merge_codex_config.py
python3 tests/test_install_codex_api.py
python3 tests/test_install_cc_api.py
python3 tests/test_install_proxy.py
python3 tests/test_shell_startup_skill_structure.py
python3 tests/test_install_shell_startup_skills.py
```

## Notes

- Template files are sanitized placeholders only
- Codex config installation merges helper-managed sections rather than replacing the whole file
- Skill installers copy guidance into Codex or Claude Code without editing shell startup files
- More Linux environment customizations such as Vim config can be added later
