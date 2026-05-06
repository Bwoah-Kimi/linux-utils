# Claude Companion

Use this companion when Claude Code is asked to clean up Bash or Zsh startup files.

## Workflow

1. Inspect the current startup files first. Do not rewrite blindly.
2. Classify each block as login bootstrap, interactive setup, env, PATH, aliases, functions, tool-managed, machine-local, or shell-specific.
3. Propose a split layout before editing.
4. Create backups before mutating any file.
5. Preserve tool-managed blocks exactly when feasible.
6. Rewrite toward the shared layout in `../references/layout.md`.
7. Use `../references/migration-heuristics.md` for ambiguous snippets.
8. Use `../references/examples.md` when you need a before and after pattern.

## Safety Rules

- keep `.bashrc` and `.zshrc` thin
- do not move Bash-only syntax into shared files
- do not move Zsh-only syntax into shared files
- keep `.zshenv` minimal
- do not drop unknown content without explaining it
- report backups, created files, modified files, and manual review items
