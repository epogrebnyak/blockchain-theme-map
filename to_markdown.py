#!/usr/bin/env python3
"""Render the Document from document.py to a Markdown file (index.md)."""

from pathlib import Path

from document import Card, Document, Item, document


def items_to_markdown(items: list[Item]) -> str:
    lines: list[str] = []
    for item in items:
        if item.is_header:
            lines.append(f"\n**{item.line}**\n")
        else:
            suffix = f" — {item.comment}" if item.comment else ""
            lines.append(f"- {item.line}{suffix}")
    return "\n".join(lines)


def card_to_markdown(card: Card) -> str:
    parts: list[str] = [f"### {card.title}\n"]
    parts.append(items_to_markdown(card.items))
    return "\n".join(parts)


def document_to_markdown(doc: Document) -> str:
    parts: list[str] = [
        f"# {doc.title}\n",
        f"*Last revision: {doc.last_revision}*\n",
        f"Source: <{doc.url}>\n",
    ]
    for section in doc.sections:
        parts.append(f"\n## {section.title}\n")
        if section.subtitle:
            parts.append(f"*{section.subtitle}*\n")
        for card in section.cards:
            parts.append(f"\n{card_to_markdown(card)}\n")
    return "\n".join(parts)


def main() -> None:
    output_path = Path(__file__).resolve().parent / "index.md"
    output_path.write_text(document_to_markdown(document), encoding="utf-8")
    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
