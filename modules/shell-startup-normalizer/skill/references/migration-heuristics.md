# Migration Heuristics

Use this file when the current startup files are noisy or mixed together.

## Classification Hints

- aliases: lines starting with `alias `, plus small alias groups under obvious alias comments
- functions: `name() { ... }`, `function name { ... }`, helper wrappers, shell utilities
- env setup: `export NAME=...`, variable defaults, editor or locale settings
- PATH setup: `export PATH=...`, helper functions that prepend or append directories, Homebrew path setup
- login bootstrap: sourcing `~/.profile`, display manager environment, session bootstrap
- interactive setup: prompt/theme init, completion, keybindings, `set -o vi`, `bind`, shell options

## Preserve Tool-Managed Blocks

Treat these as tool-managed unless the user explicitly asks you to rewrite them:

- Conda initialize blocks
- oh-my-posh init
- Homebrew `shellenv`
- oh-my-zsh, zinit, antidote, antibody, starship, powerlevel10k
- pyenv, rbenv, nvm, fnm, direnv, asdf, sdkman

Preserve the block contents exactly when feasible. If you move one, explain why and keep the content intact.

## Shell-Specific Warnings

- Bash arrays, `shopt`, and Bash completion belong in Bash files
- Zsh `autoload`, `setopt`, `typeset`, prompt themes, and plugin manager glue belong in Zsh files
- avoid putting aliases, prompts, or expensive commands into `~/.zshenv`
- avoid network calls and chatty commands in startup files for either shell

## Rewrite Strategy

- thin the entry files first
- move portable exports into `~/.shell_env`
- move aliases into `~/.shell_aliases`
- move shared helpers into `~/.shell_functions`
- keep unclear or risky blocks in the original shell-specific file until reviewed
- preserve meaningful comments, but collapse boilerplate noise

## Backup Expectations

Create timestamped backups before editing, and include the backup paths in the migration summary.
