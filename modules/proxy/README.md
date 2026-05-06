# proxy

`proxy` manages HTTP, HTTPS, and SOCKS proxy environment snippets for Linux/WSL shells.

## Contents

```text
bin/proxy                  executable helper
install/install_proxy.sh   installer for the executable and shell wrapper
```

## Install

Canonical module installer:

```bash
bash modules/proxy/install/install_proxy.sh
```

Root compatibility wrapper:

```bash
bash install/install_proxy.sh
```

## What the installer does

- copies `bin/proxy` to `~/.local/bin/proxy`
- inserts or updates a managed `proxy()` wrapper block in `~/.bash_functions`
- preserves unrelated shell functions
- warns if `~/.bashrc` does not appear to source `~/.bash_functions`

Reload your shell or run `source ~/.bash_functions` after installation.

## Usage

```bash
proxy on [--host HOST] [--port PORT] [--scheme SCHEME]
proxy off
proxy resolve [--host HOST] [--port PORT] [--scheme SCHEME]
proxy status
```

The executable emits shell commands for `on` and `off`; the installed shell function evaluates those snippets in the current shell.

Environment overrides:

- `PROXY_HOST`
- `PROXY_PORT`, default `7897`
- `PROXY_SCHEME`, default `http`
