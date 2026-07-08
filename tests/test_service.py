import asyncio
import importlib

from nhvrcontrib import service
from nhvrcontrib.errors import NhvrToolsError


def test_service_import_path_is_clean() -> None:
    service_module = importlib.import_module("nhvrcontrib.service")
    sdk_module = importlib.import_module("nhvrcontrib.sdk")

    assert hasattr(service_module, "get_fatigue_rules_data")
    assert hasattr(sdk_module, "NHVR")


def test_server_import_path_is_clean() -> None:
    server_module = importlib.import_module("nhvrcontrib.server")
    assert hasattr(server_module, "run_server")


def test_mcp_server_display_name_uses_contrib_branding() -> None:
    server_module = importlib.import_module("nhvrcontrib.server")

    mcp = server_module.mcp
    name = getattr(mcp, "name", None) or getattr(getattr(mcp, "settings", None), "name", None)

    assert name == "NHVR Contrib Tools"


def test_registration_lookup_requires_api_key() -> None:
    result = asyncio.run(service.search_vehicle_registration_data("ABC123"))

    assert result["error"]["code"] == "missing_api_key"
    assert "NHVR API key" in result["error"]["message"]


def test_registration_lookup_validates_plate_number() -> None:
    result = asyncio.run(service.search_vehicle_registration_data("!!!", api_key="test-key"))

    assert result["error"]["code"] == "invalid_plate_number"


def test_search_returns_static_fallback_when_live_search_fails(monkeypatch) -> None:
    async def fail_live_search(url: str, scraper_name: str | None) -> dict:
        raise NhvrToolsError(
            message="Playwright is required for NHVR scraping features.",
            code="missing_playwright",
        )

    monkeypatch.setattr(service, "_scrape_topic_data", fail_live_search)

    result = asyncio.run(service.search_regulations_data("bfm rest breaks"))

    assert result["matched_topic"] == "Fatigue Management"
    assert result["search_mode"] == "static_fallback"
    assert result["source_type"] == "static_fallback"
    assert result["data"]["summary"].startswith("Basic Fatigue Management")
    assert result["data"]["provenance"]["source_url"].startswith("https://")
    assert result["provenance"]["source_type"] == "static_knowledge"
    assert result["provenance"]["last_verified"] == "2026-04-11"


def test_search_returns_static_fallback_for_law_topic(monkeypatch) -> None:
    async def fail_live_search(url: str, scraper_name: str | None) -> dict:
        raise NhvrToolsError(
            message="Playwright is required for NHVR scraping features.",
            code="missing_playwright",
        )

    monkeypatch.setattr(service, "_scrape_topic_data", fail_live_search)

    result = asyncio.run(service.search_regulations_data("hvnl law"))

    assert result["matched_topic"] == "HVNL and Regulations"
    assert result["search_mode"] == "static_fallback"
    assert "Heavy Vehicle National Law" in result["data"]["summary"]
    assert result["data"]["provenance"]["source_url"].endswith("heavy-vehicle-national-law-and-regulations")


def test_search_returns_static_fallback_for_pbs_topic(monkeypatch) -> None:
    async def fail_live_search(url: str, scraper_name: str | None) -> dict:
        raise NhvrToolsError(
            message="Playwright is required for NHVR scraping features.",
            code="missing_playwright",
        )

    monkeypatch.setattr(service, "_scrape_topic_data", fail_live_search)

    result = asyncio.run(service.search_regulations_data("pbs"))

    assert result["matched_topic"] == "Performance Based Standards"
    assert result["search_mode"] == "static_fallback"
    assert "Performance Based Standards" in result["data"]["summary"]
    assert result["data"]["provenance"]["source_url"].endswith("performance-based-standards")


def test_search_returns_suggestions_for_unknown_queries() -> None:
    result = asyncio.run(service.search_regulations_data("banana wizard"))

    assert result["message"] == "No close NHVR topic match was found."
    assert len(result["suggestions"]) == 3


def test_search_live_scrape_includes_scraped_at_and_source_type(monkeypatch) -> None:
    async def succeed_live_search(url: str, scraper_name: str | None) -> dict:
        return {"url": url, "title": "Fatigue", "text": "summary"}

    monkeypatch.setattr(service, "_scrape_topic_data", succeed_live_search)

    result = asyncio.run(service.search_regulations_data("bfm rest breaks"))

    assert result["search_mode"] == "live_scrape"
    assert result["source_type"] == "live_scrape"
    assert result["scraped_at"].endswith("Z")
    assert "T" in result["scraped_at"]


def test_search_fallback_markdown_surfaces_provenance_footer(monkeypatch) -> None:
    from nhvrcontrib.formatters import format_response

    async def fail_live_search(url: str, scraper_name: str | None) -> dict:
        raise NhvrToolsError(
            message="Playwright is required for NHVR scraping features.",
            code="missing_playwright",
        )

    monkeypatch.setattr(service, "_scrape_topic_data", fail_live_search)

    result = asyncio.run(service.search_regulations_data("bfm rest breaks"))
    rendered = format_response(result, "markdown")

    assert "_Source type: static fallback_" in rendered
    assert "(verified 2026-04-11)" in rendered
    assert "_Fallback reason:" in rendered


def test_scrape_page_reports_missing_playwright(monkeypatch) -> None:
    scraper_module = importlib.import_module("nhvrcontrib.scraper")

    def fail_playwright():
        raise NhvrToolsError(
            message="Playwright is required for NHVR scraping features.",
            code="missing_playwright",
        )

    monkeypatch.setattr(scraper_module, "_get_async_playwright", fail_playwright)

    result = asyncio.run(service.scrape_page_data("https://www.nhvr.gov.au/road-access/access-permits"))

    assert result["error"]["code"] == "missing_playwright"
