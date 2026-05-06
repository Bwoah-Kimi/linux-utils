#!/usr/bin/env bash

print_step() {
    printf '==> %s\n' "$*"
}

ensure_dir() {
    mkdir -p "$1"
}

require_existing_dir() {
    if [[ ! -d "$1" ]]; then
        printf 'missing required directory: %s\n' "$1" >&2
        exit 1
    fi
}

backup_file() {
    local path="$1"
    local stamp=""

    if [[ ! -e "$path" ]]; then
        return 0
    fi

    stamp="$(date +%Y%m%d%H%M%S)"
    cp "$path" "${path}.bak.${stamp}"
}

backup_path() {
    local path="$1"
    local stamp=""

    if [[ ! -e "$path" ]]; then
        return 0
    fi

    stamp="$(date +%Y%m%d%H%M%S)"
    mv "$path" "${path}.bak.${stamp}"
}

copy_file() {
    cp "$1" "$2"
}

set_executable() {
    chmod 755 "$1"
}

find_python() {
    if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys' >/dev/null 2>&1; then
        printf 'python3\n'
        return 0
    fi
    if command -v python >/dev/null 2>&1 && python -c 'import sys' >/dev/null 2>&1; then
        printf 'python\n'
        return 0
    fi
    printf 'missing required Python interpreter\n' >&2
    exit 1
}
