"""Shared data access helpers for the SDK, CLI, and MCP tools."""

from __future__ import annotations

from typing import Any

from nhvrcontrib.api_client import NhvrApiClient
from nhvrcontrib.errors import NhvrToolsError, as_error_response
from nhvrcontrib.knowledge import (
    ACCREDITATION_INFO,
    BREACH_CATEGORIES,
    COR_DUTIES,
    DIMENSION_LIMITS,
    FATIGUE_RULES,
    HML_INFO,
    LAW_AND_REGULATIONS_INFO,
    MASS_LIMITS,
    PBS_INFO,
    PERMIT_TYPES,
    SPEED_LIMITS,
    attach_provenance,
)
from nhvrcontrib.search_index import find_topic_match, normalize_search_query, suggest_topics


def get_fatigue_rules_data(scheme: str = "standard") -> dict[str, Any]:
    if scheme not in FATIGUE_RULES:
        return _invalid_choice("fatigue scheme", scheme, FATIGUE_RULES.keys())
    return attach_provenance(FATIGUE_RULES[scheme], "fatigue_rules")


def get_mass_limits_data(include_hml: bool = False) -> dict[str, Any]:
    data: dict[str, Any] = {"general": MASS_LIMITS["general"]}
    if include_hml:
        data["hml"] = MASS_LIMITS["hml"]
    return attach_provenance(data, "mass_limits")


def get_dimension_limits_data() -> dict[str, Any]:
    return attach_provenance(DIMENSION_LIMITS, "dimension_limits")


def get_breach_categories_data(breach_type: str | None = None) -> dict[str, Any]:
    if breach_type is None:
        return attach_provenance(BREACH_CATEGORIES, "breach_categories")
    if breach_type not in BREACH_CATEGORIES or _is_metadata_key(breach_type):
        return _invalid_choice("breach type", breach_type, BREACH_CATEGORIES.keys())
    data = _with_section_reference(
        {breach_type: BREACH_CATEGORIES[breach_type]},
        BREACH_CATEGORIES.get("section_reference"),
    )
    return attach_provenance(data, "breach_categories")


def get_speed_limits_data() -> dict[str, Any]:
    return attach_provenance(SPEED_LIMITS, "speed_limits")


def get_cor_duties_data(role: str | None = None) -> dict[str, Any]:
    if role is None:
        return attach_provenance(COR_DUTIES, "cor_duties")
    if role not in COR_DUTIES or _is_metadata_key(role):
        return _invalid_choice("CoR role", role, COR_DUTIES.keys())
    data = _with_section_reference({role: COR_DUTIES[role]}, COR_DUTIES.get("section_reference"))
    return attach_provenance(data, "cor_duties")


def get_accreditation_info_data(module: str | None = None) -> dict[str, Any]:
    if module is None:
        return attach_provenance(ACCREDITATION_INFO, "accreditation_info")
    if module not in ACCREDITATION_INFO or _is_metadata_key(module):
        return _invalid_choice("accreditation module", module, ACCREDITATION_INFO.keys())
    data = _with_section_reference({module: ACCREDITATION_INFO[module]}, ACCREDITATION_INFO.get("section_reference"))
    return attach_provenance(data, "accreditation_info")


def get_permit_types_data(permit_type: str | None = None) -> dict[str, Any]:
    if permit_type is None:
        return attach_provenance(PERMIT_TYPES, "permit_types")
    if permit_type not in PERMIT_TYPES or _is_metadata_key(permit_type):
        return _invalid_choice("permit type", permit_type, PERMIT_TYPES.keys())
    data = _with_section_reference({permit_type: PERMIT_TYPES[permit_type]}, PERMIT_TYPES.get("section_reference"))
    return attach_provenance(data, "permit_types")


def get_hml_info_data() -> dict[str, Any]:
    return attach_provenance(HML_INFO, "hml_info")


def get_law_and_regulations_info_data() -> dict[str, Any]:
    return attach_provenance(LAW_AND_REGULATIONS_INFO, "law_and_regulations_info")


def get_pbs_info_data() -> dict[str, Any]:
    return attach_provenance(PBS_INFO, "pbs_info")


async def search_vehicle_registration_data(plate_number: str, api_key: str | None = None) -> dict[str, Any]:
    client = NhvrApiClient(api_key=api_key)
    try:
        return await client.search_vehicle_registration(plate_number)
    except Exception as error:
        return as_error_response(error, "Registration lookup failed.")


async def search_regulations_data(query: str) -> dict[str, Any]:
    normalized_query = normalize_search_query(query)
    if not normalized_query:
        return NhvrToolsError(
            message="Enter a search query.",
            suggestion="Try terms like `bfm`, `rest breaks`, `b-double mass`, or `oversize permits`.",
            code="empty_query",
        ).to_dict()

    match = find_topic_match(query)
    if match is None:
        return {
            "query": query,
            "message": "No close NHVR topic match was found.",
            "suggestions": suggest_topics(query),
        }

    result: dict[str, Any] = {
        "query": query,
        "matched_topic": match.topic.title,
        "matched_alias": match.alias,
        "source_url": match.topic.url,
    }

    fallback_data = _build_search_fallback(match.topic.key, normalized_query)
    try:
        live_data = await _scrape_topic_data(match.topic.url, match.topic.scraper_name)
        result["search_mode"] = "live_scrape"
        result.update(live_data)
        return result
    except Exception as error:
        if fallback_data is not None:
            result["search_mode"] = "static_fallback"
            result["fallback_reason"] = _friendly_error_message(error)
            result["data"] = fallback_data
            return result

        result.update(as_error_response(error, "Live NHVR search failed."))
        result["suggestions"] = suggest_topics(query)
        return result


async def scrape_page_data(url: str) -> dict[str, Any]:
    try:
        from nhvrcontrib.scraper import is_nhvr_url, scrape_nhvr_page
    except Exception as error:
        return as_error_response(error, "Scraper setup failed.")

    if not is_nhvr_url(url):
        return NhvrToolsError(
            message="URL must be on nhvr.gov.au.",
            suggestion="Use an official NHVR page URL such as `https://www.nhvr.gov.au/road-access/access-permits`.",
            code="invalid_url",
        ).to_dict()

    try:
        page = await scrape_nhvr_page(url, use_playwright=True)
        return {
            "url": page.url,
            "title": page.title,
            "text": page.text[:2000],
            "tables": page.tables[:5],
            "links": page.links[:20],
        }
    except Exception as error:
        return as_error_response(error, "NHVR page scrape failed.")


async def _scrape_topic_data(url: str, scraper_name: str | None) -> dict[str, Any]:
    import nhvrcontrib.scraper as scraper_module

    if scraper_name:
        scraper_function = getattr(scraper_module, scraper_name)
        parsed = await scraper_function(url, use_playwright=True)
        return {"url": url, **parsed}

    page = await scraper_module.scrape_nhvr_page(url, use_playwright=True)
    return {
        "url": page.url,
        "title": page.title,
        "text": page.text[:2000],
    }


def _build_search_fallback(topic_key: str, normalized_query: str) -> dict[str, Any] | None:
    if topic_key == "fatigue":
        if "bfm" in normalized_query:
            return get_fatigue_rules_data("bfm")
        if "afm" in normalized_query:
            return get_fatigue_rules_data("afm")
        return get_fatigue_rules_data("standard")

    if topic_key == "mass_limits":
        if "hml" in normalized_query or "higher mass" in normalized_query:
            return get_hml_info_data()
        include_hml = "b double" in normalized_query or "gross" in normalized_query
        return get_mass_limits_data(include_hml=include_hml)

    if topic_key == "dimension_requirements":
        return get_dimension_limits_data()

    if topic_key == "chain_of_responsibility":
        if "executive" in normalized_query or "due diligence" in normalized_query:
            return get_cor_duties_data("executive_duty")
        if "operator" in normalized_query:
            return get_cor_duties_data("operator")
        return get_cor_duties_data()

    if topic_key == "breach_categories":
        if "mass" in normalized_query:
            return get_breach_categories_data("mass")
        if "fatigue" in normalized_query:
            return get_breach_categories_data("fatigue")
        return get_breach_categories_data()

    if topic_key == "speed_compliance":
        return get_speed_limits_data()

    if topic_key == "accreditation":
        if "mass" in normalized_query:
            return get_accreditation_info_data("mass")
        if "fatigue" in normalized_query:
            return get_accreditation_info_data("fatigue")
        if "maintenance" in normalized_query:
            return get_accreditation_info_data("maintenance")
        return get_accreditation_info_data()

    if topic_key == "permits":
        if "class 1" in normalized_query:
            return get_permit_types_data("class_1")
        if "class 2" in normalized_query:
            return get_permit_types_data("class_2")
        if "class 3" in normalized_query:
            return get_permit_types_data("class_3")
        if "oversize" in normalized_query:
            return get_permit_types_data("oversize")
        return get_permit_types_data()

    if topic_key == "law_and_regulations":
        return get_law_and_regulations_info_data()

    if topic_key == "pbs":
        return get_pbs_info_data()

    return None


def _friendly_error_message(error: Exception) -> str:
    if isinstance(error, NhvrToolsError):
        return error.message
    return "Live NHVR content was unavailable, so a built-in knowledge response was returned instead."


def _invalid_choice(label: str, value: str, options: Any) -> dict[str, Any]:
    valid_options = ", ".join(sorted(str(option) for option in options if not _is_metadata_key(str(option))))
    return NhvrToolsError(
        message=f"Unknown {label}: {value}.",
        suggestion=f"Valid options: {valid_options}.",
        code="invalid_option",
    ).to_dict()


def _with_section_reference(data: dict[str, Any], section_reference: str | None) -> dict[str, Any]:
    response = dict(data)
    response["section_reference"] = section_reference
    return response


def _is_metadata_key(value: str) -> bool:
    return value == "section_reference" or value.startswith("overview")
