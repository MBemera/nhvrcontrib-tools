"""NHVR website scraper."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

NHVR_DOMAIN = "nhvr.gov.au"


@dataclass
class PageContent:
    url: str
    title: str
    text: str
    tables: list[str]
    links: list[str]


def is_nhvr_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.endswith(NHVR_DOMAIN)


async def fetch_page_http(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-AU,en;q=0.9",
    }
    async with httpx.AsyncClient(timeout=60, headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


async def fetch_page_playwright(url: str) -> str:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 720},
            java_script_enabled=True,
        )
        page = await context.new_page()
        # Change wait_until to "load" and increase timeout to 60 seconds
        await page.goto(url, wait_until="load", timeout=60000)
        html = await page.content()
        await context.close()
        await browser.close()
        return html


def parse_page(url: str, html: str) -> PageContent:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else ""
    main = soup.find("main") or soup.body
    text = " ".join(chunk.strip() for chunk in main.stripped_strings) if main else ""

    tables = []
    for table in soup.find_all("table"):
        tables.append(table.get_text(" ", strip=True))

    links = []
    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        if href:
            links.append(href)

    return PageContent(url=url, title=title, text=text, tables=tables, links=links)


async def fetch_page(url: str, use_playwright: bool = False) -> str:
    if use_playwright:
        return await fetch_page_playwright(url)

    return await fetch_page_http(url)


async def scrape_nhvr_page(url: str, use_playwright: bool = False) -> PageContent:
    html = await fetch_page(url, use_playwright=use_playwright)
    return parse_page(url, html)


async def scrape_dimension_requirements(url: str, use_playwright: bool = False) -> dict:
    html = await fetch_page(url, use_playwright=use_playwright)
    from nhvr_mcp.section_parsers import parse_dimension_requirements

    parsed = parse_dimension_requirements(html)
    return {
        "title": parsed.title,
        "intro": parsed.intro,
        "sections": parsed.sections,
    }


async def scrape_mass_limits(url: str, use_playwright: bool = False) -> dict:
    html = await fetch_page(url, use_playwright=use_playwright)
    from nhvr_mcp.section_parsers import parse_mass_limits

    parsed = parse_mass_limits(html)
    return {
        "title": parsed.title,
        "intro": parsed.intro,
        "sections": parsed.sections,
    }


async def scrape_cor_duties(url: str, use_playwright: bool = False) -> dict:
    html = await fetch_page(url, use_playwright=use_playwright)
    from nhvr_mcp.section_parsers import parse_cor_duties, parse_cor_sub_page

    parsed = parse_cor_duties(html)
    result: dict = {
        "title": parsed.title,
        "intro": parsed.intro,
        "sections": parsed.sections,
        "sub_pages": parsed.sub_pages,
    }

    # Fetch key sub-pages for richer content
    sub_page_keys = {
        "primary-duty": None,
        "executive-due-diligence-duty": None,
        "other-duties": None,
    }
    for label, sub_url in parsed.sub_pages.items():
        for key in sub_page_keys:
            if key in sub_url and sub_page_keys[key] is None:
                sub_page_keys[key] = sub_url

    detailed_sections: dict[str, dict] = {}
    for key, sub_url in sub_page_keys.items():
        if sub_url:
            try:
                sub_html = await fetch_page(sub_url, use_playwright=use_playwright)
                detailed_sections[key] = parse_cor_sub_page(sub_html)
            except Exception:
                pass

    if detailed_sections:
        result["detailed_sections"] = detailed_sections

    return result


async def scrape_fatigue_management(url: str, use_playwright: bool = False) -> dict:
    html = await fetch_page(url, use_playwright=use_playwright)
    from nhvr_mcp.section_parsers import parse_fatigue_management

    parsed = parse_fatigue_management(html)
    return {
        "title": parsed.title,
        "intro": parsed.intro,
        "sections": parsed.sections,
        "sub_sections": parsed.sub_sections,
    }


async def scrape_breach_categorisation(url: str, use_playwright: bool = False) -> dict:
    html = await fetch_page(url, use_playwright=use_playwright)
    from nhvr_mcp.section_parsers import parse_breach_categorisation

    parsed = parse_breach_categorisation(html)
    return {
        "title": parsed.title,
        "intro": parsed.intro,
        "sections": parsed.sections,
        "sub_sections": parsed.sub_sections,
    }


async def scrape_speed_limits(url: str, use_playwright: bool = False) -> dict:
    html = await fetch_page(url, use_playwright=use_playwright)
    from nhvr_mcp.section_parsers import parse_speed_limits

    parsed = parse_speed_limits(html)
    return {
        "title": parsed.title,
        "intro": parsed.intro,
        "sections": parsed.sections,
    }


async def scrape_nhvas_info(url: str, use_playwright: bool = False) -> dict:
    html = await fetch_page(url, use_playwright=use_playwright)
    from nhvr_mcp.section_parsers import parse_nhvas_info

    parsed = parse_nhvas_info(html)
    return {
        "title": parsed.title,
        "intro": parsed.intro,
        "sections": parsed.sections,
    }


async def scrape_permit_types(url: str, use_playwright: bool = False) -> dict:
    html = await fetch_page(url, use_playwright=use_playwright)
    from nhvr_mcp.section_parsers import parse_permit_types

    parsed = parse_permit_types(html)
    return {
        "title": parsed.title,
        "intro": parsed.intro,
        "sections": parsed.sections,
    }
