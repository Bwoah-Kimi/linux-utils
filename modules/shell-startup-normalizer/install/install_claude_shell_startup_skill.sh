#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${MODULE_ROOT}/../.." && pwd)"

# shellcheck source=/dev/null
source "${REPO_ROOT}/shared/install_common.sh"

HOME_DIR="${HOME:?HOME must be set}"
SKILLS_DIR="${HOME_DIR}/.claude/skills"
TARGET_DIR="${SKILLS_DIR}/shell-startup-normalizer"
SOURCE_DIR="${MODULE_ROOT}/skill"

print_step "Installing shell-startup-normalizer for Claude Code"
ensure_dir "${SKILLS_DIR}"

backup_path "${TARGET_DIR}"
cp -R "${SOURCE_DIR}" "${TARGET_DIR}"

printf 'Installed: %s\n' "${TARGET_DIR}"
printf 'Usage: ask Claude Code to normalize messy shell startup files using %s/claude/CLAUDE.md\n' "${TARGET_DIR}"
