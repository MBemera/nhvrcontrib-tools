"""NHVR Python SDK for programmatic access to heavy vehicle compliance data."""

from __future__ import annotations

import os

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


class NHVR:
    """Client for querying NHVR heavy vehicle compliance data.

    Sync methods return dicts from the built-in knowledge base.
    Async methods (search_registration, search, scrape) require ``await``.
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("NHVR_API_KEY")

    # -- Sync knowledge-base lookups --

    def fatigue_rules(self, scheme: str = "standard") -> dict:
        return get_fatigue_rules_data(scheme=scheme)

    def mass_limits(self, include_hml: bool = False) -> dict:
        return get_mass_limits_data(include_hml=include_hml)

    def dimension_limits(self) -> dict:
        return get_dimension_limits_data()

    def breach_categories(self, breach_type: str | None = None) -> dict:
        return get_breach_categories_data(breach_type=breach_type)

    def speed_limits(self) -> dict:
        return get_speed_limits_data()

    def cor_duties(self, role: str | None = None) -> dict:
        return get_cor_duties_data(role=role)

    def accreditation(self, module: str | None = None) -> dict:
        return get_accreditation_info_data(module=module)

    def permit_types(self, permit_type: str | None = None) -> dict:
        return get_permit_types_data(permit_type=permit_type)

    def hml_info(self) -> dict:
        return get_hml_info_data()

    # -- Async methods (network) --

    async def search_registration(self, plate_number: str) -> dict:
        return await search_vehicle_registration_data(plate_number=plate_number, api_key=self.api_key)

    async def search(self, query: str) -> dict:
        return await search_regulations_data(query=query)

    async def scrape(self, url: str) -> dict:
        return await scrape_page_data(url=url)
