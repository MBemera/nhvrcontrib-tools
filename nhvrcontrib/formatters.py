"""Formatting helpers for tool responses."""

from __future__ import annotations

import json
from typing import Any

SPECIAL_LABELS = {
    "afm": "AFM",
    "api": "API",
    "bfm": "BFM",
    "cor": "CoR",
    "hml": "HML",
    "hvnl": "HVNL",
    "mcp": "MCP",
    "nhvas": "NHVAS",
    "url": "URL",
}


SOURCE_TYPE_LABELS = {
    "static_knowledge": "static knowledge",
    "live_scrape": "live scrape",
    "static_fallback": "static fallback",
}


def format_response(data: Any, output_format: str) -> str:
    if output_format == "json":
        return json.dumps({"data": data}, indent=2, sort_keys=True)

    return render_markdown(data).strip()


def render_markdown(data: Any, depth: int = 2) -> str:
    provenance = None
    live_footer_lines: list[str] = []
    content = data

    if isinstance(data, dict):
        content = dict(data)
        provenance = content.pop("provenance", None)
        live_footer_lines = _extract_live_footer_lines(content)

        nested_data = content.get("data")
        if isinstance(nested_data, dict) and "provenance" in nested_data:
            nested_copy = dict(nested_data)
            if provenance is None:
                provenance = nested_copy.pop("provenance", None)
            else:
                nested_copy.pop("provenance", None)
            content["data"] = nested_copy

    lines = _render_block(content, depth)
    footer_lines = _render_provenance_footer(provenance)
    combined_footer = live_footer_lines + footer_lines
    if combined_footer:
        if lines:
            lines.append("")
        lines.extend(combined_footer)

    return "\n".join(lines)


def _extract_live_footer_lines(content: dict[str, Any]) -> list[str]:
    source_type = content.get("source_type")
    if source_type not in {"live_scrape", "static_fallback"}:
        return []

    scraped_at = content.pop("scraped_at", None)
    fallback_reason = content.pop("fallback_reason", None)
    content.pop("source_type", None)

    lines: list[str] = []
    label = SOURCE_TYPE_LABELS.get(str(source_type), str(source_type))
    lines.append(f"_Source type: {label}_")

    if isinstance(scraped_at, str) and scraped_at:
        lines.append(f"_Scraped: {scraped_at}_")

    if source_type == "static_fallback" and isinstance(fallback_reason, str) and fallback_reason:
        lines.append(f"_Fallback reason: {fallback_reason}_")

    return lines


def _render_block(data: Any, depth: int, label: str | None = None) -> list[str]:
    if isinstance(data, dict):
        return _render_dict(data, depth, label)
    if isinstance(data, list):
        return _render_list(data, depth, label)
    return _render_scalar(data, label)


def _render_dict(data: dict[str, Any], depth: int, label: str | None) -> list[str]:
    lines: list[str] = []
    heading_label = _format_label(label) if label else None
    if heading_label:
        lines.append(f"{'#' * min(depth, 6)} {heading_label}")

    scalar_items: list[tuple[str, Any]] = []
    nested_items: list[tuple[str, Any]] = []
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            nested_items.append((key, value))
            continue
        scalar_items.append((key, value))

    for key, value in scalar_items:
        lines.append(f"- {_format_label(key)}: {_stringify(value)}")

    child_depth = min(depth + 1, 6) if heading_label else depth
    for key, value in nested_items:
        if lines:
            lines.append("")
        lines.extend(_render_block(value, child_depth, key))

    return lines or ["- None"]


def _render_list(data: list[Any], depth: int, label: str | None) -> list[str]:
    lines: list[str] = []
    heading_label = _format_label(label) if label else None
    if heading_label:
        lines.append(f"{'#' * min(depth, 6)} {heading_label}")

    for item in data:
        if isinstance(item, (dict, list)):
            item_lines = _render_block(item, min(depth + 1, 6))
            first_line, *remaining_lines = item_lines
            lines.append(f"- {first_line}")
            for line in remaining_lines:
                lines.append(f"  {line}")
            continue
        lines.append(f"- {_stringify(item)}")

    return lines or ["- None"]


def _render_scalar(data: Any, label: str | None) -> list[str]:
    if label:
        return [f"- {_format_label(label)}: {_stringify(data)}"]
    return [_stringify(data)]


def _format_label(value: str) -> str:
    cleaned_value = value.replace("-", " ").replace("_", " ").strip()
    words = []
    for word in cleaned_value.split():
        lower_word = word.lower()
        words.append(SPECIAL_LABELS.get(lower_word, word.capitalize()))
    return " ".join(words) or value


def _stringify(value: Any) -> str:
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value)


def _render_provenance_footer(provenance: Any) -> list[str]:
    if not isinstance(provenance, dict):
        return []

    source_title = provenance.get("source_title")
    source_url = provenance.get("deep_link_url") or provenance.get("source_url")
    last_verified = provenance.get("last_verified")
    source_type = provenance.get("source_type")
    section_reference = provenance.get("section_reference")

    footer_lines: list[str] = []
    if isinstance(source_title, str) and isinstance(source_url, str) and isinstance(last_verified, str):
        footer_lines.append(f"_Source: [{source_title}]({source_url}) (verified {last_verified})_")

    if isinstance(source_type, str) and source_type:
        label = SOURCE_TYPE_LABELS.get(source_type, source_type)
        footer_lines.append(f"_Source type: {label}_")

    if isinstance(section_reference, str) and section_reference:
        footer_lines.append(f"_Section: {section_reference}_")

    unofficial_warning = provenance.get("unofficial_warning")
    if isinstance(unofficial_warning, str) and unofficial_warning:
        footer_lines.append(f"_{unofficial_warning}_")

    return footer_lines
