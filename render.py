#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

GROUP_SPECS = [
    {
        "class": "group1",
        "id": "group-1-title",
        "badge": "Group 1",
        "title": "Use Cases",
        "note": "Horizontal cards occupy the full content width.",
        "horizontal": True,
        "cards": [
            {"title": "What users need blockchain for?", "subtitle": "Use cases"},
        ],
    },
    {
        "class": "layer2",
        "id": "layer-2-title",
        "badge": "Layer 2",
        "title": "Minimal Blockchain",
        "note": "Each card is horizontal and spans the full content width.",
        "horizontal": True,
        "cards": [
            {"title": "Transactions", "subtitle": "Transactions"},
            {"title": "Assets", "subtitle": "Assets and contract types"},
            {"title": "Network economics", "subtitle": "Incentives"},
            {"title": "Chains and ecosystems", "subtitle": "Networks"},
            {"title": "Core technology", "subtitle": "Foundations"},
        ],
    },
    {
        "class": "layer3",
        "id": "layer-3-title",
        "badge": "Layer 3",
        "title": "User Access and Custody",
        "note": "",
        "horizontal": False,
        "cards": [
            {"title": "Wallets and key management", "subtitle": "Wallets and key management"},
            {"title": "Institutional custody", "subtitle": "Institutional custody"},
        ],
    },
    {
        "class": "layer4",
        "id": "layer-4-title",
        "badge": "Layer 4",
        "title": "Network Enhancements",
        "note": "",
        "horizontal": False,
        "cards": [
            {"title": "Cross-network communication", "subtitle": "Interoperability"},
            {"title": "External data", "subtitle": "Oracles and data feeds"},
            {"title": "Data persistence", "subtitle": "Storage"},
        ],
    },
    {
        "class": "layer5",
        "id": "layer-5-title",
        "badge": "Layer 5",
        "title": "Features and Protection",
        "note": "Three categories.",
        "horizontal": False,
        "cards": [
            {"title": "Privacy and user protection", "subtitle": "Privacy and user protection"},
            {"title": "System protection", "subtitle": "Contract security"},
            {"title": "Compliance", "subtitle": "Compliance"},
        ],
    },
    {
        "class": "layer6",
        "id": "layer-6-title",
        "badge": "Layer 6",
        "title": "Risk Management",
        "note": "Horizontal cards occupy the full content width.",
        "horizontal": True,
        "cards": [
            {"title": "Lessons learned", "subtitle": "Past incidents"},
            {"title": "Persistent threats", "subtitle": "Risk categories"},
        ],
    },
]


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
    orientation = payload.get("_orientation")

    if orientation == "table":
        return {
            "title": title,
            "subtitle": subtitle,
            "layout": "table",
            "rows": parse_rows(payload),
        }

    if "items" in payload and payload["items"] and all(isinstance(item, str) for item in payload["items"]):
        return {
            "title": title,
            "subtitle": subtitle,
            "layout": "list",
            "items": payload["items"],
        }

    return {
        "title": title,
        "subtitle": subtitle,
        "layout": "blocks",
        "blocks": parse_blocks(payload),
    }


def extract_meta(text: str, pattern: str, fallback: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def build_context(data: dict[str, Any], source_text: str) -> dict[str, Any]:
    groups = []
    for spec in GROUP_SPECS:
        cards = []
        for card in spec["cards"]:
            subtitle = card["subtitle"]
            payload = data.get(subtitle)
            if not isinstance(payload, dict):
                raise ValueError(f"Card data not found or invalid for '{subtitle}'")
            cards.append(parse_card(card["title"], subtitle, payload))

        groups.append(
            {
                "class": spec["class"],
                "id": spec["id"],
                "badge": spec["badge"],
                "title": spec["title"],
                "note": spec["note"],
                "horizontal": spec["horizontal"],
                "cards": cards,
            }
        )

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
