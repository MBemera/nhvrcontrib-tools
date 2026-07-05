"""Section-specific parsers for NHVR pages."""

from __future__ import annotations

from dataclasses import dataclass, field

from bs4 import BeautifulSoup

NHVR_BASE_URL = "https://www.nhvr.gov.au"


@dataclass
class ParsedPage:
    """Structured content extracted from an NHVR page."""

    title: str
    intro: str
    sections: dict[str, str]
    sub_sections: dict[str, dict[str, str]] = field(default_factory=dict)
    sub_pages: dict[str, str] = field(default_factory=dict)


def parse_sections_page(
    html: str,
    default_title: str,
    *,
    include_sub_sections: bool = False,
    sub_page_path: str | None = None,
) -> ParsedPage:
    """Parse an NHVR page into intro text and h2 (optionally h2/h3) sections.

    ``sub_page_path`` collects links whose href contains that fragment, for
    pages that spread their content across sub-pages.
    """
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else default_title
    main = soup.find("main") or soup.body

    if not main:
        return ParsedPage(title=title, intro="", sections={})

    return ParsedPage(
        title=title,
        intro=get_intro_text(main),
        sections=get_h2_sections(main),
        sub_sections=get_h2_h3_sections(main) if include_sub_sections else {},
        sub_pages=_get_sub_page_links(main, sub_page_path) if sub_page_path else {},
    )


def parse_dimension_requirements(html: str) -> ParsedPage:
    return parse_sections_page(html, "Dimension requirements")


def parse_mass_limits(html: str) -> ParsedPage:
    return parse_sections_page(html, "Mass limits")


def parse_cor_duties(html: str) -> ParsedPage:
    """Parse the Chain of Responsibility main page, including sub-page links."""
    return parse_sections_page(html, "Chain of Responsibility", sub_page_path="chain-of-responsibility/")


def parse_cor_sub_page(html: str) -> dict[str, str]:
    """Parse a CoR sub-page (primary duty, other duties, etc.)."""
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup.body
    if not main:
        return {}
    return get_h2_sections(main)


def parse_fatigue_management(html: str) -> ParsedPage:
    """Parse the Fatigue Management page (main or work-and-rest-requirements)."""
    return parse_sections_page(html, "Fatigue management", include_sub_sections=True)


def parse_breach_categorisation(html: str) -> ParsedPage:
    return parse_sections_page(html, "Breach categorisation", include_sub_sections=True)


def parse_speed_limits(html: str) -> ParsedPage:
    return parse_sections_page(html, "Speed limits")


def parse_nhvas_info(html: str) -> ParsedPage:
    return parse_sections_page(html, "NHVAS")


def parse_permit_types(html: str) -> ParsedPage:
    return parse_sections_page(html, "Access permits")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def get_intro_text(main) -> str:
    first_paragraph = main.find("p")
    if not first_paragraph:
        return ""

    return first_paragraph.get_text(" ", strip=True)


def get_h2_sections(main) -> dict[str, str]:
    sections: dict[str, str] = {}
    headings = main.find_all("h2")
    for heading in headings:
        section_title = heading.get_text(" ", strip=True)
        section_text = get_section_text(heading)
        if section_text:
            sections[section_title] = section_text
    return sections


def get_h2_h3_sections(main) -> dict[str, dict[str, str]]:
    """Extract h2 sections with their h3 sub-sections nested."""
    result: dict[str, dict[str, str]] = {}
    for h2 in main.find_all("h2"):
        h2_title = h2.get_text(" ", strip=True)
        h3_map: dict[str, str] = {}
        for sibling in h2.find_next_siblings():
            if sibling.name == "h2":
                break
            if sibling.name == "h3":
                h3_title = sibling.get_text(" ", strip=True)
                h3_text = get_section_text(sibling, stop_tags={"h2", "h3"})
                if h3_text:
                    h3_map[h3_title] = h3_text
        if h3_map:
            result[h2_title] = h3_map
    return result


def get_section_text(heading, stop_tags: set[str] | None = None) -> str:
    if stop_tags is None:
        stop_tags = {"h2"}
    content_parts = []
    for sibling in heading.find_next_siblings():
        if sibling.name in stop_tags:
            break
        if sibling.name in {"p", "ul", "ol"}:
            content_parts.append(sibling.get_text(" ", strip=True))
    return "\n".join(content_parts).strip()


def _get_sub_page_links(main, path_fragment: str) -> dict[str, str]:
    sub_pages: dict[str, str] = {}
    for anchor in main.find_all("a", href=True):
        href = anchor["href"]
        if path_fragment not in href:
            continue
        link_text = anchor.get_text(strip=True)[:80]
        if not link_text:
            continue
        if href.startswith("/"):
            href = NHVR_BASE_URL + href
        sub_pages[link_text] = href
    return sub_pages
