"""MCP server entrypoint for NHVR tools."""

from __future__ import annotations

import os

from fastmcp import FastMCP

from nhvrcontrib.formatters import format_response
from nhvrcontrib.service import (
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

mcp = FastMCP("NHVR Contrib Tools")


@mcp.tool
async def nhvr_search_vehicle_registration(plate_number: str, output_format: str = "markdown") -> str:
    """Vehicle registration lookup. Monitored by NHVR; intended for operator fleet management, not bulk extracts."""
    data = await search_vehicle_registration_data(plate_number=plate_number)
    return format_response(data, output_format)


@mcp.tool
async def nhvr_get_fatigue_rules(scheme: str = "standard", output_format: str = "markdown") -> str:
    """Work and rest hour requirements by scheme (standard, bfm, afm)."""
    return format_response(get_fatigue_rules_data(scheme=scheme), output_format)


@mcp.tool
async def nhvr_get_mass_limits(include_hml: bool = False, output_format: str = "markdown") -> str:
    """General mass limits, with optional Higher Mass Limits data."""
    return format_response(get_mass_limits_data(include_hml=include_hml), output_format)


@mcp.tool
async def nhvr_get_dimension_limits(output_format: str = "markdown") -> str:
    """Heavy vehicle dimension limits (height, width, length, overhang)."""
    return format_response(get_dimension_limits_data(), output_format)


@mcp.tool
async def nhvr_get_breach_categories(breach_type: str | None = None, output_format: str = "markdown") -> str:
    """Breach severity categories, optionally filtered by breach type (mass, dimension, loading, fatigue, speed)."""
    return format_response(get_breach_categories_data(breach_type=breach_type), output_format)


@mcp.tool
async def nhvr_get_speed_limits(output_format: str = "markdown") -> str:
    """Heavy vehicle speed limits and speed limiter rules."""
    return format_response(get_speed_limits_data(), output_format)


@mcp.tool
async def nhvr_get_cor_duties(role: str | None = None, output_format: str = "markdown") -> str:
    """Chain of Responsibility duties, optionally filtered by role."""
    return format_response(get_cor_duties_data(role=role), output_format)


@mcp.tool
async def nhvr_get_accreditation_info(module: str | None = None, output_format: str = "markdown") -> str:
    """NHVAS and HVA accreditation guidance, optionally filtered by module."""
    return format_response(get_accreditation_info_data(module=module), output_format)


@mcp.tool
async def nhvr_get_permit_types(permit_type: str | None = None, output_format: str = "markdown") -> str:
    """Access permit guidance, optionally filtered by permit type."""
    return format_response(get_permit_types_data(permit_type=permit_type), output_format)


@mcp.tool
async def nhvr_get_hml_info(output_format: str = "markdown") -> str:
    """Higher Mass Limits eligibility, limits, and application guidance."""
    return format_response(get_hml_info_data(), output_format)


@mcp.tool
async def nhvr_search_regulations(query: str, output_format: str = "markdown") -> str:
    """Natural-language NHVR topic search with live scraping and static fallback."""
    data = await search_regulations_data(query=query)
    return format_response(data, output_format)


@mcp.tool
async def nhvr_scrape_page(url: str, output_format: str = "markdown") -> str:
    """Scrape a specific nhvr.gov.au page."""
    data = await scrape_page_data(url=url)
    return format_response(data, output_format)


def run_server() -> None:
    transport = os.getenv("NHVR_MCP_TRANSPORT", "stdio")
    if transport == "streamable_http":
        host = os.getenv("NHVR_MCP_HOST", "0.0.0.0")
        port = int(os.getenv("NHVR_MCP_PORT", "8080"))
        mcp.run(transport="streamable_http", host=host, port=port)
        return

    mcp.run()


if __name__ == "__main__":
    run_server()
