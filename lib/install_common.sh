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

copy_file() {
    cp "$1" "$2"
}

set_executable() {
    chmod 755 "$1"
}
