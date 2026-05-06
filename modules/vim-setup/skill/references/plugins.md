# Plugins

All plugins are managed by Vundle and declared in `.vimrc` between `vundle#begin()` and `vundle#end()`.

## Plugin List

### Vundle.vim

- **Declaration:** `Plugin 'VundleVim/Vundle.vim'`
- **Purpose:** Plugin manager. Manages itself and all other plugins.
- **Notes:** Must be bootstrapped first via git clone before any `:PluginInstall` can run.

### gruvbox

- **Declaration:** `Plugin 'morhetz/gruvbox'`
- **Purpose:** Retro groove colorscheme with dark and light variants.
- **Notes:** Applied via `autocmd vimenter * ++nested colorscheme gruvbox` with `set background=dark`.

### sparkup

- **Declaration:** `Plugin 'rstacruz/sparkup'`
- **Purpose:** Write HTML in CSS-like syntax and expand it. Type `div.container>ul>li*3` and press Ctrl+E to expand.
- **Notes:** Useful for quick HTML authoring.

### vim-fugitive

- **Declaration:** `Plugin 'tpope/vim-fugitive'`
- **Purpose:** Git integration inside Vim. Provides `:Git` commands for status, diff, blame, commit, and more.
- **Notes:** No extra configuration needed.

## Installing Plugins

After writing the `.vimrc` and bootstrapping Vundle:

```bash
vim +PluginInstall +qall
```

This runs Vim in batch mode, installs all declared plugins, and exits.

## Adding New Plugins

To add a plugin, insert a `Plugin` line inside the Vundle block and run `:PluginInstall` from within Vim or re-run the batch command above.
