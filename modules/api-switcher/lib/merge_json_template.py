#!/usr/bin/env python3
from __future__ import annotations
"""Merge a JSON template into an existing JSON file.

Keys present in the target are kept as-is (existing values, including real API
keys, are never overwritten). Keys present in the template but missing from the
target are added with their template values (typically placeholders).

Usage: merge_json_template.py <target> <template>
"""
import json
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        fail("usage: merge_json_template.py <target> <template>")

    target_path = Path(argv[0])
    template_path = Path(argv[1])

    try:
        template = json.loads(template_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"failed to read template {template_path}: {exc}")

    if not isinstance(template, dict):
        fail(f"expected JSON object in {template_path}")

    if target_path.exists():
        try:
            existing = json.loads(target_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"failed to read {target_path}: {exc}")
        if not isinstance(existing, dict):
            fail(f"expected JSON object in {target_path}")
        for key, value in template.items():
            if key not in existing:
                existing[key] = value
        result = existing
    else:
        result = template

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
