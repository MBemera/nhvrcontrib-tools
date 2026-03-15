"""NHVR API client."""

from __future__ import annotations

import os

import httpx


class NhvrApiClient:
    def __init__(self) -> None:
        self.base_url = "https://api-public.nhvr.gov.au"
        self.api_key = os.getenv("NHVR_API_KEY")

    async def search_vehicle_registration(self, plate_number: str) -> dict:
        headers = {}
        if self.api_key:
            headers["Ocp-Apim-Subscription-Key"] = self.api_key

        url = f"{self.base_url}/vehicles/registration/{plate_number}"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
