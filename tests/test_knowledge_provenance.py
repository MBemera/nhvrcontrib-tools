from nhvrcontrib.formatters import format_response
from nhvrcontrib.service import (
    get_accreditation_info_data,
    get_breach_categories_data,
    get_cor_duties_data,
    get_dimension_limits_data,
    get_fatigue_rules_data,
    get_hml_info_data,
    get_law_and_regulations_info_data,
    get_mass_limits_data,
    get_pbs_info_data,
    get_permit_types_data,
    get_speed_limits_data,
)


def test_all_sync_responses_include_last_verified_date() -> None:
    responses = [
        get_fatigue_rules_data("standard"),
        get_mass_limits_data(include_hml=True),
        get_dimension_limits_data(),
        get_breach_categories_data(),
        get_speed_limits_data(),
        get_cor_duties_data(),
        get_accreditation_info_data(),
        get_permit_types_data(),
        get_hml_info_data(),
        get_law_and_regulations_info_data(),
        get_pbs_info_data(),
    ]

    for response in responses:
        assert response["provenance"]["last_verified"] == "2026-04-11"


def test_markdown_uses_deep_link_when_section_reference_is_available() -> None:
    response = get_cor_duties_data("operator")
    rendered = format_response(response, "markdown")

    assert "https://www.legislation.qld.gov.au/view/whole/html/inforce/current/act-2012-hvnlq#sec.26C" in rendered
    assert "_Source: [NHVR chain of responsibility guidance]" in rendered
