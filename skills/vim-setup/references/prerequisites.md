# Prerequisites

## Required Packages

### vim-gtk3 (Debian/Ubuntu)

Provides Vim compiled with `+clipboard` and `+xterm_clipboard` support, required for `set clipboard=unnamedplus` to work.

**Install:**

```bash
sudo apt install vim-gtk3
```

**Verify:**

```bash
vim --version | grep clipboard
```

Expected output should show `+clipboard` (not `-clipboard`).

**Other distros:**

- Fedora/RHEL: `sudo dnf install vim-X11` (provides `vimx`)
- Arch: `sudo pacman -S gvim` (the gvim package includes clipboard support)

### git

Required for bootstrapping Vundle and installing plugins.

**Verify:**

```bash
git --version
```

## Vundle Bootstrap

If `~/.vim/bundle/Vundle.vim` does not exist, bootstrap it:

```bash
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

Do not re-clone if the directory already exists.

## WSL Notes

On WSL2, `vim-gtk3` provides clipboard support that bridges to the Windows clipboard. The system clipboard (`+` register) works for copy/paste between Vim and Windows applications.
