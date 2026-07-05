import asyncio

import pytest

from nhvrcontrib import scraper
from nhvrcontrib.errors import NhvrToolsError
from nhvrcontrib.section_parsers import ParsedPage


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.nhvr.gov.au/road-access/access-permits", True),
        ("https://service.nhvr.gov.au/road-access/access-permits", True),
        ("https://www.nhvr.gov.au:443/road-access/access-permits", True),
        ("https://faknhvr.gov.au/road-access/access-permits", False),
        ("not-a-url", False),
    ],
)
def test_is_nhvr_url(url: str, expected: bool) -> None:
    assert scraper.is_nhvr_url(url) is expected


def test_scrape_cor_duties_reports_partial_sub_page_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    main_url = "https://www.nhvr.gov.au/safety-accreditation-compliance/chain-of-responsibility"
    primary_url = f"{main_url}/primary-duty"
    other_url = f"{main_url}/other-duties"

    async def fake_fetch_page(url: str, use_playwright: bool = False) -> str:
        if url == main_url:
            return "<html><body><main>Main page</main></body></html>"
        if url == primary_url:
            return "<html><body><main>Primary duty</main></body></html>"
        raise NhvrToolsError(message="Other duties page is unavailable.", code="site_unavailable")

    monkeypatch.setattr(scraper, "fetch_page", fake_fetch_page)

    import nhvrcontrib.section_parsers as section_parsers

    monkeypatch.setattr(
        section_parsers,
        "parse_cor_duties",
        lambda html: ParsedPage(
            title="Chain of Responsibility",
            intro="Intro",
            sections={"Overview": "Summary"},
            sub_pages={
                "Primary duty": primary_url,
                "Other duties": other_url,
            },
        ),
    )
    monkeypatch.setattr(section_parsers, "parse_cor_sub_page", lambda html: {"Heading": "Parsed text"})

    result = asyncio.run(scraper.scrape_cor_duties(main_url))

    assert result["detailed_sections"]["primary-duty"] == {"Heading": "Parsed text"}
    assert result["detailed_sections_errors"] == {"other-duties": "Other duties page is unavailable."}
