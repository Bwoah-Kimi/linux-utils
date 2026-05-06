#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${MODULE_ROOT}/../.." && pwd)"

# shellcheck source=/dev/null
source "${REPO_ROOT}/shared/install_common.sh"

HOME_DIR="${HOME:?HOME must be set}"
CLAUDE_DIR="${HOME_DIR}/.claude"
BIN_DIR="${HOME_DIR}/.local/bin"
TARGET_SCRIPT="${BIN_DIR}/cc_api"
TARGET_PROVIDER_LIST="${CLAUDE_DIR}/provider_list.json"

print_step "Installing cc_api"
require_existing_dir "${CLAUDE_DIR}"
ensure_dir "${BIN_DIR}"

backup_file "${TARGET_SCRIPT}"
backup_file "${TARGET_PROVIDER_LIST}"

copy_file "${MODULE_ROOT}/bin/cc_api" "${TARGET_SCRIPT}"
set_executable "${TARGET_SCRIPT}"
PYTHON_BIN="$(find_python)"
"${PYTHON_BIN}" "${MODULE_ROOT}/lib/merge_json_template.py" \
    "${TARGET_PROVIDER_LIST}" \
    "${MODULE_ROOT}/templates/claude/provider_list.json"

printf 'Installed: %s\n' "${TARGET_SCRIPT}"
printf 'Merged providers into: %s\n' "${TARGET_PROVIDER_LIST}"
printf 'Note: existing provider tokens were preserved; new entries use placeholder values\n'
printf 'Preserved existing Claude settings in %s/settings.json\n' "${CLAUDE_DIR}"
