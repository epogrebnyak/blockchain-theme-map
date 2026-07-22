#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

TAB_WIDTH = 2
YAML_LINE_WIDTH = 1000


def load_yaml(path: Path) -> Any:
    source_text = path.read_text(encoding="utf-8")
    normalized_text = source_text.expandtabs(TAB_WIDTH)
    try:
        return yaml.safe_load(normalized_text)
    except yaml.YAMLError as exc:
        raise ValueError(f"Unable to parse YAML file: {path}: {exc}") from exc


def build_content(root_path: Path) -> list[dict[str, Any]]:
    root_data = load_yaml(root_path)
    if root_data is None:
        return []
    if not isinstance(root_data, list):
        raise ValueError(f"{root_path} must contain a YAML list")

    src_dir = root_path.parent
    sections: list[dict[str, Any]] = []
    for index, entry in enumerate(root_data, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"Item #{index} in {root_path} must be a mapping")
        file_name = entry.get("file")
        if not isinstance(file_name, str) or not file_name.strip():
            raise ValueError(f"Item #{index} in {root_path} is missing a valid 'file' field")

        section_path = (src_dir / file_name).resolve()
        section_data = load_yaml(section_path)

        section = {k: v for k, v in entry.items() if k != "file"}
        section["content"] = section_data
        sections.append(section)

    return sections


def write_content(output_path: Path, sections: list[dict[str, Any]]) -> None:
    output_path.write_text(
        yaml.safe_dump(sections, sort_keys=False, allow_unicode=True, width=YAML_LINE_WIDTH),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build content.yaml from src/root.yaml and referenced files")
    parser.add_argument("--root", default="src/root.yaml", help="Path to root YAML file")
    parser.add_argument("--output", default="content.yaml", help="Path to output YAML file")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    root_path = (base_dir / args.root).resolve()
    output_path = (base_dir / args.output).resolve()

    sections = build_content(root_path)
    write_content(output_path, sections)
    print(f"Wrote {output_path} with {len(sections)} section(s)")


if __name__ == "__main__":
    main()
