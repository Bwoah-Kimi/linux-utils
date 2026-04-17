#!/usr/bin/env python3
import json
import re
import sys
import tomllib
from pathlib import Path


SECTION_RE = re.compile(r"^\[([^\]]+)\]\s*$")
MODEL_PROVIDER_RE = re.compile(r'(?m)^model_provider\s*=\s*"[^"]*"\s*$')


def fail(message: str) -> "None":
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_toml_text(path: Path) -> tuple[dict, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"failed to read {path}: {exc}")

    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        fail(f"malformed TOML in {path}: {exc}")
    return data, text


def render_toml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value)
    fail(f"unsupported TOML value type: {type(value).__name__}")


def render_provider_blocks(providers: dict[str, dict[str, object]]) -> str:
    blocks: list[str] = []
    for provider_name, provider_config in providers.items():
        block_lines = [f"[model_providers.{provider_name}]"]
        for key, value in provider_config.items():
            block_lines.append(f"{key} = {render_toml_value(value)}")
        blocks.append("\n".join(block_lines))
    return "\n\n".join(blocks).rstrip("\n")


def strip_provider_sections(text: str) -> str:
    kept_lines: list[str] = []
    skipping = False

    for line in text.splitlines(keepends=True):
        match = SECTION_RE.match(line.strip())
        if match:
            section_name = match.group(1)
            if section_name.startswith("model_providers."):
                skipping = True
                continue
            skipping = False
        if skipping:
            continue
        kept_lines.append(line)
    return "".join(kept_lines)


def replace_model_provider(text: str, provider_name: str) -> str:
    updated, count = MODEL_PROVIDER_RE.subn(
        f'model_provider = "{provider_name}"',
        text,
        count=1,
    )
    if count == 1:
        return updated
    return f'model_provider = "{provider_name}"\n{updated}'


def insert_provider_blocks(text: str, provider_blocks: str) -> str:
    lines = text.splitlines(keepends=True)
    first_section_index = len(lines)
    for index, line in enumerate(lines):
        if SECTION_RE.match(line.strip()):
            first_section_index = index
            break

    prefix = "".join(lines[:first_section_index]).strip("\n")
    suffix = "".join(lines[first_section_index:]).strip("\n")

    parts = [part for part in (prefix, provider_blocks.strip("\n"), suffix) if part]
    return "\n\n".join(parts) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        fail("usage: merge_codex_config.py <local-config> <provider-config>")

    local_path = Path(argv[0])
    provider_path = Path(argv[1])

    _, local_text = load_toml_text(local_path)
    provider_data, _ = load_toml_text(provider_path)

    provider_name = provider_data.get("model_provider")
    providers = provider_data.get("model_providers")

    if not isinstance(provider_name, str) or not provider_name:
        fail(f"missing model_provider in {provider_path}")
    if not isinstance(providers, dict) or not providers:
        fail(f"missing model_providers in {provider_path}")

    without_provider_sections = strip_provider_sections(local_text)
    with_provider_name = replace_model_provider(without_provider_sections, provider_name)
    provider_blocks = render_provider_blocks(providers)
    merged_text = insert_provider_blocks(with_provider_name, provider_blocks)
    local_path.write_text(merged_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
