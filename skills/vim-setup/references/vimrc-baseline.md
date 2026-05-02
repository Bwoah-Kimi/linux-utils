# Baseline .vimrc

This is the target `.vimrc` content. When setting up Vim, write this file or merge its sections into an existing `.vimrc`.

## Full Baseline

```vim
set nocompatible
filetype off

" Vundle setup
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'morhetz/gruvbox'
Plugin 'rstacruz/sparkup'
Plugin 'tpope/vim-fugitive'

call vundle#end()
filetype plugin indent on

" Colorscheme
autocmd vimenter * ++nested colorscheme gruvbox
set background=dark

" Editor settings
set foldmethod=syntax
set hlsearch
set cursorline
set clipboard=unnamedplus
```

## Section Notes

### Vundle Block

The Vundle block must appear before any `filetype plugin indent on` call. `set nocompatible` and `filetype off` are required before `vundle#begin()`. All `Plugin` declarations go between `vundle#begin()` and `vundle#end()`.

### Colorscheme

`autocmd vimenter * ++nested colorscheme gruvbox` applies gruvbox after all plugins load. The `++nested` flag allows nested autocommands so gruvbox can set highlight groups correctly. `set background=dark` selects the dark variant.

### Editor Settings

- `foldmethod=syntax` — folds based on language syntax
- `hlsearch` — highlights all matches when searching
- `cursorline` — highlights the line the cursor is on
- `clipboard=unnamedplus` — yank, delete, and paste use the system clipboard (requires Vim compiled with `+clipboard`)

## Merging With Existing Config

If the user has an existing `.vimrc` with additional settings:

1. Preserve any user-added settings that are not in the baseline
2. Ensure the Vundle block is at the top, before `filetype plugin indent on`
3. Add any missing `Plugin` declarations inside the Vundle block
4. Add any missing editor settings after the Vundle block
5. Do not duplicate settings that already exist
