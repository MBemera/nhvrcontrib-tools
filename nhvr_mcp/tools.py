"""Tool implementations for NHVR MCP."""

from __future__ import annotations

from nhvr_mcp.formatters import format_response
from nhvr_mcp.service import (
    get_accreditation_info_data,
    get_breach_categories_data,
    get_cor_duties_data,
    get_dimension_limits_data,
    get_fatigue_rules_data,
    get_hml_info_data,
    get_mass_limits_data,
    get_permit_types_data,
    get_speed_limits_data,
    scrape_page_data,
    search_regulations_data,
    search_vehicle_registration_data,
)


def get_fatigue_rules(scheme: str, output_format: str) -> str:
    data = get_fatigue_rules_data(scheme=scheme)
    return format_response(data, output_format)


def get_mass_limits(include_hml: bool, output_format: str) -> str:
    data = get_mass_limits_data(include_hml=include_hml)
    return format_response(data, output_format)


def get_dimension_limits(output_format: str) -> str:
    return format_response(get_dimension_limits_data(), output_format)


def get_breach_categories(breach_type: str | None, output_format: str) -> str:
    data = get_breach_categories_data(breach_type=breach_type)
    return format_response(data, output_format)


def get_speed_limits(output_format: str) -> str:
    return format_response(get_speed_limits_data(), output_format)


def get_cor_duties(role: str | None, output_format: str) -> str:
    data = get_cor_duties_data(role=role)
    return format_response(data, output_format)


def get_accreditation_info(module: str | None, output_format: str) -> str:
    data = get_accreditation_info_data(module=module)
    return format_response(data, output_format)


def get_permit_types(permit_type: str | None, output_format: str) -> str:
    data = get_permit_types_data(permit_type=permit_type)
    return format_response(data, output_format)


def get_hml_info(output_format: str) -> str:
    return format_response(get_hml_info_data(), output_format)


async def search_vehicle_registration(plate_number: str, output_format: str) -> str:
    data = await search_vehicle_registration_data(plate_number=plate_number)
    return format_response(data, output_format)


async def search_regulations(query: str, output_format: str) -> str:
    data = await search_regulations_data(query=query)
    return format_response(data, output_format)


async def scrape_page(url: str, output_format: str) -> str:
    data = await scrape_page_data(url=url)
    return format_response(data, output_format)
