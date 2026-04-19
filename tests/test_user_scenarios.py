import asyncio
import json
from typing import Any

import pytest
from click.testing import CliRunner

from nhvrcontrib import NHVR, service
from nhvrcontrib.cli import cli
from nhvrcontrib.errors import NhvrToolsError
from nhvrcontrib.formatters import format_response


def get_nested_value(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    current_value: Any = data
    for key in path:
        current_value = current_value[key]
    return current_value


def build_cli_runner() -> CliRunner:
    return CliRunner()


def force_search_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fail_live_search(url: str, scraper_name: str | None) -> dict[str, Any]:
        raise NhvrToolsError(
            message="Playwright is required for NHVR scraping features.",
            code="missing_playwright",
        )

    monkeypatch.setattr(service, "_scrape_topic_data", fail_live_search)


def _run_missing_playwright_scrape(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    scraper_module = pytest.importorskip("nhvrcontrib.scraper")

    def fail_playwright():
        raise NhvrToolsError(
            message="Playwright is required for NHVR scraping features.",
            code="missing_playwright",
        )

    monkeypatch.setattr(scraper_module, "_get_async_playwright", fail_playwright)
    return asyncio.run(service.scrape_page_data("https://www.nhvr.gov.au/road-access/access-permits"))


def _assert_search_fallback_metadata(monkeypatch: pytest.MonkeyPatch) -> bool:
    force_search_fallback(monkeypatch)
    result = asyncio.run(service.search_regulations_data("rest breaks"))
    return (
        result["search_mode"] == "static_fallback"
        and "fallback_reason" in result
        and result["source_url"].startswith("https://")
    )


def _assert_cli_json_provenance(monkeypatch: pytest.MonkeyPatch) -> bool:
    runner = build_cli_runner()
    result = runner.invoke(cli, ["--format", "json", "fatigue", "rules"])
    if result.exit_code != 0:
        return False
    payload = json.loads(result.output)
    return "provenance" in payload["data"]


@pytest.mark.parametrize(
    ("method_name", "kwargs", "path", "expected_text"),
    [
        ("fatigue_rules", {"scheme": "standard"}, ("summary",), "Standard hours"),
        ("fatigue_rules", {"scheme": "bfm"}, ("summary",), "Basic Fatigue Management"),
        ("fatigue_rules", {"scheme": "afm"}, ("description",), "only mechanism under the HVNL"),
        ("mass_limits", {}, ("general", "summary"), "General Mass Limits"),
        ("mass_limits", {"include_hml": True}, ("general", "b_double_26m_example"), "62.5 t"),
        ("dimension_limits", {}, ("height",), "4.3 m"),
        ("breach_categories", {"breach_type": "mass"}, ("mass", "minor"), "≤5%"),
        ("speed_limits", {}, ("speed_limiter", "requirement"), "100 km/h"),
        ("cor_duties", {"role": "operator"}, ("operator",), "Operators must ensure"),
        ("permit_types", {"permit_type": "oversize"}, ("oversize", "summary"), "Oversize/overmass permits"),
    ],
)
def test_sdk_user_scenarios(
    method_name: str,
    kwargs: dict[str, Any],
    path: tuple[str, ...],
    expected_text: str,
) -> None:
    client = NHVR()
    method = getattr(client, method_name)

    result = method(**kwargs)

    assert expected_text in get_nested_value(result, path)
    assert "provenance" in result


@pytest.mark.parametrize(
    ("args", "expected_text"),
    [
        (["--help"], "Usage:"),
        (["fatigue", "rules"], "Summary"),
        (["fatigue", "rules", "--scheme", "afm"], "Advanced Fatigue Management"),
        (["mass", "limits"], "General Mass Limits"),
        (["mass", "limits", "--include-hml"], "22.5 t"),
        (["dimension", "limits"], "Height"),
        (["breach", "categories", "--type", "fatigue"], "Critical"),
        (["cor", "duties", "--role", "operator"], "Operators must ensure"),
        (["permits", "--type", "oversize"], "Oversize/overmass permits"),
        (["--format", "json", "speed"], '"speed_limiter"'),
    ],
)
def test_cli_user_scenarios(args: list[str], expected_text: str) -> None:
    runner = build_cli_runner()

    result = runner.invoke(cli, args)

    assert result.exit_code == 0
    assert expected_text in result.output


@pytest.mark.parametrize(
    ("query", "expected_topic", "path", "expected_text"),
    [
        ("bfm", "Fatigue Management", ("data", "summary"), "Basic Fatigue Management"),
        ("afm", "Fatigue Management", ("data", "summary"), "Advanced Fatigue Management"),
        ("rest breaks", "Fatigue Management", ("data", "summary"), "Standard hours"),
        ("work diary rules", "Fatigue Management", ("data", "summary"), "Standard hours"),
        ("b-double mass", "Mass Limits", ("data", "general", "b_double_26m_example"), "62.5 t"),
        ("higher mass limits", "Mass Limits", ("data", "limits", "tri_axle_group"), "22.5 t"),
        ("height limit for trucks", "Dimension Requirements", ("data", "height"), "4.3 m"),
        ("rear overhang rules", "Dimension Requirements", ("data", "rear_overhang", "general"), "60%"),
        ("loader duty", "Chain of Responsibility", ("data", "overview"), "Chain of Responsibility"),
        ("executive due diligence", "Chain of Responsibility", ("data", "executive_duty"), "due diligence"),
        ("operator duties", "Chain of Responsibility", ("data", "operator"), "Operators must ensure"),
        ("mass breach categories", "Breach Categories", ("data", "mass", "minor"), "≤5%"),
        ("fatigue breach", "Breach Categories", ("data", "fatigue", "critical"), "extreme risk"),
        (
            "speed limiter",
            "Speed Compliance",
            ("data", "speed_limiter", "requirement"),
            "100 km/h",
        ),
        (
            "speed limit for heavy vehicles",
            "Speed Compliance",
            ("data", "default", "heavy_vehicle_speed_limit"),
            "posted limits and road rules",
        ),
        (
            "nhvas fatigue accreditation",
            "NHVAS Accreditation",
            ("data", "fatigue", "summary"),
            "NHVAS Fatigue Management",
        ),
        (
            "maintenance management accreditation",
            "NHVAS Accreditation",
            ("data", "maintenance", "summary"),
            "NHVAS Maintenance Management",
        ),
        ("oversize permits", "Access Permits", ("data", "oversize", "summary"), "Oversize/overmass permits"),
        ("class 1 permit", "Access Permits", ("data", "class_1", "summary"), "Class 1 heavy vehicle"),
        ("class 3 permit route approval", "Access Permits", ("data", "class_3", "note"), "Route-specific permits"),
    ],
)
def test_search_user_scenarios(
    monkeypatch: pytest.MonkeyPatch,
    query: str,
    expected_topic: str,
    path: tuple[str, ...],
    expected_text: str,
) -> None:
    force_search_fallback(monkeypatch)

    result = asyncio.run(service.search_regulations_data(query))

    assert result["matched_topic"] == expected_topic
    assert result["search_mode"] == "static_fallback"
    assert expected_text in get_nested_value(result, path)


@pytest.mark.parametrize(
    ("scenario_name", "operation", "expected_code", "expected_text"),
    [
        (
            "missing_api_key",
            lambda monkeypatch: asyncio.run(service.search_vehicle_registration_data("ABC123")),
            "missing_api_key",
            "NHVR API key is required",
        ),
        (
            "invalid_plate",
            lambda monkeypatch: asyncio.run(service.search_vehicle_registration_data("!!!", api_key="test-key")),
            "invalid_plate_number",
            "Enter a valid plate number",
        ),
        (
            "invalid_url",
            lambda monkeypatch: asyncio.run(service.scrape_page_data("https://example.com/not-nhvr")),
            "invalid_url",
            "URL must be on nhvr.gov.au.",
        ),
        (
            "missing_playwright",
            _run_missing_playwright_scrape,
            "missing_playwright",
            "Playwright is required",
        ),
        (
            "empty_query",
            lambda monkeypatch: asyncio.run(service.search_regulations_data("   ")),
            "empty_query",
            "Enter a search query.",
        ),
    ],
)
def test_error_user_scenarios(
    monkeypatch: pytest.MonkeyPatch,
    scenario_name: str,
    operation,
    expected_code: str,
    expected_text: str,
) -> None:
    result = operation(monkeypatch)

    assert result["error"]["code"] == expected_code
    assert expected_text in result["error"]["message"]


@pytest.mark.parametrize(
    ("scenario_name", "assertion"),
    [
        (
            "markdown_mass_limits",
            lambda monkeypatch: (
                "## General" in format_response(NHVR().mass_limits(include_hml=True), "markdown")
                and "_Source: [" in format_response(NHVR().mass_limits(include_hml=True), "markdown")
            ),
        ),
        (
            "json_speed_output",
            lambda monkeypatch: "posted limits and road rules" in json.loads(
                format_response(NHVR().speed_limits(), "json")
            )["data"]["default"]["heavy_vehicle_speed_limit"],
        ),
        (
            "sdk_provenance_fields",
            lambda monkeypatch: {
                "source_title",
                "source_url",
                "last_verified",
                "unofficial_warning",
            }.issubset(NHVR().fatigue_rules("standard")["provenance"]),
        ),
        (
            "search_fallback_metadata",
            _assert_search_fallback_metadata,
        ),
        (
            "cli_json_provenance",
            _assert_cli_json_provenance,
        ),
    ],
)
def test_format_and_provenance_user_scenarios(
    monkeypatch: pytest.MonkeyPatch,
    scenario_name: str,
    assertion,
) -> None:
    assert assertion(monkeypatch)
