#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# shellcheck source=/dev/null
source "${REPO_ROOT}/lib/install_common.sh"

HOME_DIR="${HOME:?HOME must be set}"
CODEX_DIR="${HOME_DIR}/.codex"
BIN_DIR="${HOME_DIR}/.local/bin"
TARGET_SCRIPT="${BIN_DIR}/codex_api"
TARGET_AUTH_LIST="${CODEX_DIR}/auth_list.json"
TARGET_CONFIG="${CODEX_DIR}/config.toml"

print_step "Installing codex_api"
require_existing_dir "${CODEX_DIR}"
ensure_dir "${BIN_DIR}"

backup_file "${TARGET_SCRIPT}"
backup_file "${TARGET_AUTH_LIST}"
backup_file "${TARGET_CONFIG}"

copy_file "${REPO_ROOT}/bin/codex_api" "${TARGET_SCRIPT}"
set_executable "${TARGET_SCRIPT}"
python3 "${REPO_ROOT}/lib/merge_json_template.py" \
    "${TARGET_AUTH_LIST}" \
    "${REPO_ROOT}/templates/codex/auth_list.json"

python3 "${REPO_ROOT}/lib/merge_codex_config.py" \
    "${TARGET_CONFIG}" \
    "${REPO_ROOT}/templates/codex/config.providers.toml"

printf 'Installed: %s\n' "${TARGET_SCRIPT}"
printf 'Merged auth keys into: %s\n' "${TARGET_AUTH_LIST}"
printf 'Note: existing API keys were preserved; new entries use placeholder values\n'
printf 'Merged helper-managed providers into: %s\n' "${TARGET_CONFIG}"
