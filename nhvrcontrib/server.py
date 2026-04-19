"""MCP server entrypoint for NHVR tools."""

from __future__ import annotations

import os

from fastmcp import FastMCP

from nhvrcontrib.tools import (
    get_accreditation_info,
    get_breach_categories,
    get_cor_duties,
    get_dimension_limits,
    get_fatigue_rules,
    get_hml_info,
    get_mass_limits,
    get_permit_types,
    get_speed_limits,
    scrape_page,
    search_regulations,
    search_vehicle_registration,
)

mcp = FastMCP("NHVR Tools")


@mcp.tool
async def nhvr_search_vehicle_registration(plate_number: str, output_format: str = "markdown") -> str:
    return await search_vehicle_registration(plate_number=plate_number, output_format=output_format)


@mcp.tool
async def nhvr_get_fatigue_rules(scheme: str = "standard", output_format: str = "markdown") -> str:
    return get_fatigue_rules(scheme=scheme, output_format=output_format)


@mcp.tool
async def nhvr_get_mass_limits(include_hml: bool = False, output_format: str = "markdown") -> str:
    return get_mass_limits(include_hml=include_hml, output_format=output_format)


@mcp.tool
async def nhvr_get_dimension_limits(output_format: str = "markdown") -> str:
    return get_dimension_limits(output_format=output_format)


@mcp.tool
async def nhvr_get_breach_categories(breach_type: str | None = None, output_format: str = "markdown") -> str:
    return get_breach_categories(breach_type=breach_type, output_format=output_format)


@mcp.tool
async def nhvr_get_speed_limits(output_format: str = "markdown") -> str:
    return get_speed_limits(output_format=output_format)


@mcp.tool
async def nhvr_get_cor_duties(role: str | None = None, output_format: str = "markdown") -> str:
    return get_cor_duties(role=role, output_format=output_format)


@mcp.tool
async def nhvr_get_accreditation_info(module: str | None = None, output_format: str = "markdown") -> str:
    return get_accreditation_info(module=module, output_format=output_format)


@mcp.tool
async def nhvr_get_permit_types(permit_type: str | None = None, output_format: str = "markdown") -> str:
    return get_permit_types(permit_type=permit_type, output_format=output_format)


@mcp.tool
async def nhvr_get_hml_info(output_format: str = "markdown") -> str:
    return get_hml_info(output_format=output_format)


@mcp.tool
async def nhvr_search_regulations(query: str, output_format: str = "markdown") -> str:
    return await search_regulations(query=query, output_format=output_format)


@mcp.tool
async def nhvr_scrape_page(url: str, output_format: str = "markdown") -> str:
    return await scrape_page(url=url, output_format=output_format)


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
