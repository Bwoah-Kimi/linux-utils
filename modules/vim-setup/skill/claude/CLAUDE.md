# Claude Companion

Use this companion when Claude Code is asked to set up or restore a Vim configuration.

## Workflow

1. Inspect the current Vim setup first. Do not write blindly.
2. Check `vim --version` for clipboard support and Vim version.
3. Read `~/.vimrc` and list `~/.vim/bundle/` if they exist.
4. Report findings and missing prerequisites to the user.
5. Create timestamped backups before editing any file.
6. Write or merge the baseline `.vimrc` from `../references/vimrc-baseline.md`.
7. Bootstrap Vundle if `~/.vim/bundle/Vundle.vim` is missing: `git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim`
8. Install plugins: `vim +PluginInstall +qall`
9. Verify: confirm gruvbox loads, plugins are in `~/.vim/bundle/`, clipboard works.

## Safety Rules

- back up `~/.vimrc` and `~/.vim/` before any changes
- show the user what will change before overwriting `.vimrc`
- do not re-clone Vundle if it already exists
- do not remove plugins the user added outside the baseline
- prompt for package installs rather than running them silently
- report backups, created files, installed plugins, and manual follow-up items
