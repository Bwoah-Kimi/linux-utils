#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# shellcheck source=/dev/null
source "${REPO_ROOT}/lib/install_common.sh"

HOME_DIR="${HOME:?HOME must be set}"
BIN_DIR="${HOME_DIR}/.local/bin"
TARGET_SCRIPT="${BIN_DIR}/proxy"
BASH_FUNCTIONS="${HOME_DIR}/.bash_functions"
BASHRC="${HOME_DIR}/.bashrc"

print_step "Installing proxy"
ensure_dir "${BIN_DIR}"

backup_file "${TARGET_SCRIPT}"
backup_file "${BASH_FUNCTIONS}"

copy_file "${REPO_ROOT}/bin/proxy" "${TARGET_SCRIPT}"
set_executable "${TARGET_SCRIPT}"

[[ -f "${BASH_FUNCTIONS}" ]] || : > "${BASH_FUNCTIONS}"

python3 - "${BASH_FUNCTIONS}" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
begin = "# BEGIN linux-utils proxy wrapper"
end = "# END linux-utils proxy wrapper"
managed = """# BEGIN linux-utils proxy wrapper
proxy() {
    local action="${1:-status}"
    local shell_snippet=""

    case "${action}" in
        on|set)
            shift
            shell_snippet="$(command proxy on "$@")" || return $?
            eval "${shell_snippet}"
            command proxy status
            ;;
        off|unset)
            shift
            shell_snippet="$(command proxy off)" || return $?
            eval "${shell_snippet}"
            command proxy status
            ;;
        status)
            shift
            command proxy status "$@"
            ;;
        resolve)
            shift
            command proxy resolve "$@"
            ;;
        *)
            echo "Usage: proxy {on|off|status|resolve|set|unset} [--host HOST] [--port PORT] [--scheme SCHEME]" >&2
            return 1
            ;;
    esac
}
# END linux-utils proxy wrapper
"""

text = path.read_text(encoding="utf-8")
if begin in text and end in text:
    start = text.index(begin)
    finish = text.index(end) + len(end)
    updated = text[:start].rstrip("\n")
    suffix = text[finish:].lstrip("\n")
    parts = [part for part in (updated, managed.rstrip("\n"), suffix) if part]
    new_text = "\n\n".join(parts) + "\n"
else:
    base = text.rstrip("\n")
    parts = [part for part in (base, managed.rstrip("\n")) if part]
    new_text = "\n\n".join(parts) + "\n"

path.write_text(new_text, encoding="utf-8")
PY

if [[ -f "${BASHRC}" ]] && ! grep -q '\.bash_functions' "${BASHRC}"; then
    printf 'Warning: %s does not appear to source ~/.bash_functions\n' "${BASHRC}" >&2
fi

printf 'Installed: %s\n' "${TARGET_SCRIPT}"
printf 'Updated managed proxy wrapper block in: %s\n' "${BASH_FUNCTIONS}"
printf 'Manual step: reload your shell or source %s\n' "${BASH_FUNCTIONS}"
