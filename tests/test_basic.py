from nhvrcontrib.formatters import format_response
from nhvrcontrib.knowledge import FATIGUE_RULES
from nhvrcontrib.tools import get_fatigue_rules, get_mass_limits


def test_format_response_json():
    result = format_response({"key": "value"}, "json")
    assert "\"key\"" in result


def test_get_fatigue_rules_standard():
    result = get_fatigue_rules("standard", "markdown")
    assert FATIGUE_RULES["standard"]["summary"] in result


def test_format_response_markdown_sections():
    result = get_mass_limits(include_hml=True, output_format="markdown")

    assert "## General" in result
    assert "## HML" in result
    assert "## Provenance" not in result
    assert "_Source: [" in result
    assert "(verified 2026-04-11)" in result
