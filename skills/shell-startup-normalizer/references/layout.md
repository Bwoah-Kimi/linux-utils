# Target Layout

Use this file when deciding where each shell startup concern should live.

## Shared Files

- `~/.shell_env`: portable environment variables, PATH helpers, shared exports
- `~/.shell_aliases`: aliases only
- `~/.shell_functions`: reusable helper functions that are safe across shells
- `~/.shell_local`: machine-local overrides kept out of the portable baseline

These files should be sourced with existence guards.

## Bash Files

- `~/.bash_profile`: login-shell bootstrap, `~/.profile` integration when needed, source `~/.shell_env`, then hand off to `~/.bashrc` for interactive shells
- `~/.bashrc`: interactive guard near the top, source `~/.shell_env`, `~/.shell_aliases`, `~/.shell_functions`, preserve interactive tool init, then source local overrides

If the machine already uses `~/.bash_aliases` or `~/.bash_functions`, migration can keep transitional guarded sourcing until the user is ready to delete those files.

## Zsh Files

- `~/.zprofile`: login-shell bootstrap and shared env loading
- `~/.zshrc`: interactive setup, aliases, functions, prompt, plugins, completions, local overrides
- `~/.zshenv`: keep minimal and rare; only variables that must exist for every Zsh invocation

Keep plugin managers and themes in `~/.zshrc` unless there is a shell-specific reason to do otherwise.

## Load Order Guidance

Preferred order for interactive shells:

1. interactive guard where appropriate
2. shared env
3. shared aliases
4. shared functions
5. shell-specific interactive setup
6. tool-managed interactive blocks
7. machine-local overrides

Local override files should usually be last so the user has a clear escape hatch.
