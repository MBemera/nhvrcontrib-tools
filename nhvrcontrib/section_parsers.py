"""Section-specific parsers for NHVR pages."""

from __future__ import annotations

from dataclasses import dataclass, field

from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class DimensionRequirements:
    title: str
    intro: str
    sections: dict[str, str]


@dataclass
class MassLimits:
    title: str
    intro: str
    sections: dict[str, str]


@dataclass
class CorDuties:
    title: str
    intro: str
    sections: dict[str, str]
    sub_pages: dict[str, str] = field(default_factory=dict)


@dataclass
class FatigueManagement:
    title: str
    intro: str
    sections: dict[str, str]
    sub_sections: dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass
class BreachCategorisation:
    title: str
    intro: str
    sections: dict[str, str]
    sub_sections: dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass
class SpeedLimits:
    title: str
    intro: str
    sections: dict[str, str]


@dataclass
class NhvasInfo:
    title: str
    intro: str
    sections: dict[str, str]


@dataclass
class PermitTypes:
    title: str
    intro: str
    sections: dict[str, str]


# ---------------------------------------------------------------------------
# Parser functions
# ---------------------------------------------------------------------------


def parse_dimension_requirements(html: str) -> DimensionRequirements:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else "Dimension requirements"
    main = soup.find("main") or soup.body

    if not main:
        return DimensionRequirements(title=title, intro="", sections={})

    return DimensionRequirements(
        title=title,
        intro=get_intro_text(main),
        sections=get_h2_sections(main),
    )


def parse_mass_limits(html: str) -> MassLimits:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else "Mass limits"
    main = soup.find("main") or soup.body

    if not main:
        return MassLimits(title=title, intro="", sections={})

    return MassLimits(
        title=title,
        intro=get_intro_text(main),
        sections=get_h2_sections(main),
    )


def parse_cor_duties(html: str) -> CorDuties:
    """Parse the Chain of Responsibility main page."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else "Chain of Responsibility"
    main = soup.find("main") or soup.body

    if not main:
        return CorDuties(title=title, intro="", sections={})

    # Extract sub-page links for further navigation
    sub_pages: dict[str, str] = {}
    for a in main.find_all("a", href=True):
        href = a["href"]
        if "chain-of-responsibility/" in href:
            link_text = a.get_text(strip=True)[:80]
            if link_text:
                if href.startswith("/"):
                    href = "https://www.nhvr.gov.au" + href
                sub_pages[link_text] = href

    return CorDuties(
        title=title,
        intro=get_intro_text(main),
        sections=get_h2_sections(main),
        sub_pages=sub_pages,
    )


def parse_cor_sub_page(html: str) -> dict[str, str]:
    """Parse a CoR sub-page (primary duty, other duties, etc.)."""
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup.body
    if not main:
        return {}
    return get_h2_sections(main)


def parse_fatigue_management(html: str) -> FatigueManagement:
    """Parse the Fatigue Management page (main or work-and-rest-requirements)."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else "Fatigue management"
    main = soup.find("main") or soup.body

    if not main:
        return FatigueManagement(title=title, intro="", sections={})

    sections = get_h2_sections(main)
    sub_sections = get_h2_h3_sections(main)

    return FatigueManagement(
        title=title,
        intro=get_intro_text(main),
        sections=sections,
        sub_sections=sub_sections,
    )


def parse_breach_categorisation(html: str) -> BreachCategorisation:
    """Parse the Breach Categorisation page."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else "Breach categorisation"
    main = soup.find("main") or soup.body

    if not main:
        return BreachCategorisation(title=title, intro="", sections={})

    sections = get_h2_sections(main)
    sub_sections = get_h2_h3_sections(main)

    return BreachCategorisation(
        title=title,
        intro=get_intro_text(main),
        sections=sections,
        sub_sections=sub_sections,
    )


def parse_speed_limits(html: str) -> SpeedLimits:
    """Parse the Speed/Speeding page."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else "Speed limits"
    main = soup.find("main") or soup.body

    if not main:
        return SpeedLimits(title=title, intro="", sections={})

    return SpeedLimits(
        title=title,
        intro=get_intro_text(main),
        sections=get_h2_sections(main),
    )


def parse_nhvas_info(html: str) -> NhvasInfo:
    """Parse the NHVAS page."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else "NHVAS"
    main = soup.find("main") or soup.body

    if not main:
        return NhvasInfo(title=title, intro="", sections={})

    return NhvasInfo(
        title=title,
        intro=get_intro_text(main),
        sections=get_h2_sections(main),
    )


def parse_permit_types(html: str) -> PermitTypes:
    """Parse the Access Permits page."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else "Access permits"
    main = soup.find("main") or soup.body

    if not main:
        return PermitTypes(title=title, intro="", sections={})

    return PermitTypes(
        title=title,
        intro=get_intro_text(main),
        sections=get_h2_sections(main),
    )


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
