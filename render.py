#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

DEFAULT_GROUP = "Themes"
VALID_ORIENTATIONS = {"horizontal", "vertical", "table"}


def to_lines(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        lines: list[str] = []
        for item in value:
            if isinstance(item, str):
                lines.append(item)
        return lines
    return []


def parse_blocks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if "items" in payload:
        blocks: list[dict[str, Any]] = []
        for item in payload["items"]:
            if not isinstance(item, dict) or not item:
                continue
            title, value = next(iter(item.items()))
            blocks.append({"title": title, "items": to_lines(value)})
        return blocks

    blocks = []
    for key, value in payload.items():
        if key == "_orientation":
            continue
        blocks.append({"title": key, "items": to_lines(value)})
    return blocks


def parse_rows(payload: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in payload.get("items", []):
        if not isinstance(item, dict) or not item:
            continue

        category, details = next(iter(item.items()))
        description = ""
        example = ""

        if isinstance(details, str):
            description = details
        elif isinstance(details, list):
            if details:
                first = details[0]
                description = first if isinstance(first, str) else ""
            for extra in details[1:]:
                if isinstance(extra, dict) and "Example" in extra:
                    example = str(extra["Example"])
                    break
                if isinstance(extra, str):
                    example = extra
                    break

        rows.append({
            "category": category,
            "description": description,
            "example": example,
        })
    return rows


def parse_card(title: str, subtitle: str, payload: dict[str, Any]) -> dict[str, Any]:
    orientation = payload.get("_orientation", "vertical")
    if not isinstance(orientation, str) or orientation not in VALID_ORIENTATIONS:
        orientation = "vertical"
    show_subtitle = subtitle != title

    if orientation == "table":
        return {
            "title": title,
            "subtitle": subtitle,
            "show_subtitle": show_subtitle,
            "orientation": orientation,
            "layout": "table",
            "rows": parse_rows(payload),
        }

    if "items" in payload and payload["items"] and all(isinstance(item, str) for item in payload["items"]):
        return {
            "title": title,
            "subtitle": subtitle,
            "show_subtitle": show_subtitle,
            "orientation": orientation,
            "layout": "list",
            "items": payload["items"],
        }

    return {
        "title": title,
        "subtitle": subtitle,
        "show_subtitle": show_subtitle,
        "orientation": orientation,
        "layout": "blocks",
        "blocks": parse_blocks(payload),
    }


def extract_meta(text: str, pattern: str, fallback: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def parse_outline(source_text: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    group_pattern = re.compile(r"^#\s*(?:GROUP|LAYER)\s+(?:\d+\.\s+)?(.+?)\s*$")
    card_pattern = re.compile(r"^#\s*Card\s+\d+\.\s*(.+?)\s*$")
    key_pattern = re.compile(r"^([^#\s][^:]*):\s*$")

    group_order: list[str] = []
    cards_by_subtitle: dict[str, dict[str, str]] = {}
    current_group = DEFAULT_GROUP
    pending_card_title: str | None = None

    for line in source_text.splitlines():
        group_match = group_pattern.match(line)
        if group_match:
            current_group = group_match.group(1).strip()
            if current_group not in group_order:
                group_order.append(current_group)
            pending_card_title = None
            continue

        card_match = card_pattern.match(line)
        if card_match:
            pending_card_title = card_match.group(1).strip()
            continue

        if pending_card_title:
            key_match = key_pattern.match(line)
            if key_match:
                subtitle = key_match.group(1).strip()
                cards_by_subtitle[subtitle] = {"group": current_group, "title": pending_card_title}
                pending_card_title = None

    if not group_order:
        group_order.append(DEFAULT_GROUP)

    return group_order, cards_by_subtitle


def build_context(data: dict[str, Any], source_text: str) -> dict[str, Any]:
    group_order, cards_by_subtitle = parse_outline(source_text)
    groups_map: OrderedDict[str, dict[str, Any]] = OrderedDict(
        (title, {"title": title, "cards": []}) for title in group_order
    )

    for subtitle, payload in data.items():
        if not isinstance(payload, dict):
            continue

        card_meta = cards_by_subtitle.get(subtitle, {})
        group_title = card_meta.get("group", DEFAULT_GROUP)
        card_title = card_meta.get("title", subtitle)

        if group_title not in groups_map:
            groups_map[group_title] = {"title": group_title, "cards": []}

        groups_map[group_title]["cards"].append(parse_card(card_title, subtitle, payload))

    groups = [group for group in groups_map.values() if group["cards"]]

    return {
        "groups": groups,
        "source_href": "themes.yaml",
        "source_name": "themes.yaml",
        "last_revised": extract_meta(source_text, r"^#\s*Last revision:\s*(.+)$", "July 21, 2026"),
        "repository_url": extract_meta(
            source_text,
            r"^#\s*URL:\s*(https?://\S+)\s*$",
            "https://github.com/epogrebnyak/blockchain-theme-map",
        ),
    }


def render(template_path: Path, yaml_path: Path, output_path: Path) -> None:
    source_text = yaml_path.read_text(encoding="utf-8")
    data = yaml.safe_load(source_text)
    if not isinstance(data, dict):
        raise ValueError("themes.yaml must parse to a mapping")

    context = build_context(data, source_text)

    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_path.name)
    output_path.write_text(template.render(**context), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render index.html from index.jinja2 and themes.yaml")
    parser.add_argument("--template", default="index.jinja2", help="Path to Jinja template")
    parser.add_argument("--data", default="themes.yaml", help="Path to YAML data file")
    parser.add_argument("--output", default="index.html", help="Path to output HTML file")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    template_path = (base_dir / args.template).resolve()
    yaml_path = (base_dir / args.data).resolve()
    output_path = (base_dir / args.output).resolve()

    render(template_path, yaml_path, output_path)


if __name__ == "__main__":
    main()
