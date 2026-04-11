"""NHVR API client."""

from __future__ import annotations

import os
import re

import httpx

from nhvr_mcp.errors import NhvrToolsError

PLATE_NUMBER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 -]{0,15}$")


class NhvrApiClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.base_url = "https://api-public.nhvr.gov.au"
        self.api_key = api_key or os.getenv("NHVR_API_KEY")

    async def search_vehicle_registration(self, plate_number: str) -> dict:
        normalized_plate_number = self._normalize_plate_number(plate_number)
        if not self.api_key:
            raise NhvrToolsError(
                message="NHVR API key is required for vehicle registration lookups.",
                suggestion="Set `NHVR_API_KEY` or pass `api_key=` when creating `NHVR()`.",
                code="missing_api_key",
            )

        headers = {}
        headers["Ocp-Apim-Subscription-Key"] = self.api_key

        url = f"{self.base_url}/vehicles/registration/{normalized_plate_number}"
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException as error:
            raise NhvrToolsError(
                message="The NHVR registration service timed out.",
                suggestion="Try again in a moment.",
                technical_detail=str(error),
                code="timeout",
            ) from error
        except httpx.HTTPStatusError as error:
            raise self._build_http_error(normalized_plate_number, error) from error
        except httpx.RequestError as error:
            raise NhvrToolsError(
                message="Could not reach the NHVR registration service.",
                suggestion="Check your network connection and try again.",
                technical_detail=str(error),
                code="network_error",
            ) from error

    def _normalize_plate_number(self, plate_number: str) -> str:
        normalized_plate_number = plate_number.strip().upper()
        if not normalized_plate_number or not PLATE_NUMBER_PATTERN.fullmatch(normalized_plate_number):
            raise NhvrToolsError(
                message="Enter a valid plate number using letters, numbers, spaces, or hyphens.",
                suggestion="Example: `ABC123`.",
                code="invalid_plate_number",
            )
        return normalized_plate_number

    def _build_http_error(self, plate_number: str, error: httpx.HTTPStatusError) -> NhvrToolsError:
        response = error.response
        technical_detail = response.text.strip()[:300] or None

        if response.status_code in {401, 403}:
            return NhvrToolsError(
                message="NHVR API authentication failed.",
                suggestion="Check that your NHVR API key is valid and still active.",
                technical_detail=technical_detail,
                code="authentication_failed",
            )
        if response.status_code == 404:
            return NhvrToolsError(
                message=f"No registration record was found for plate `{plate_number}`.",
                suggestion="Check the plate number and state formatting, then try again.",
                technical_detail=technical_detail,
                code="not_found",
            )
        if response.status_code == 400:
            return NhvrToolsError(
                message="The NHVR API rejected that registration lookup.",
                suggestion="Check the plate number formatting and try again.",
                technical_detail=technical_detail,
                code="bad_request",
            )
        if response.status_code == 429:
            return NhvrToolsError(
                message="The NHVR API rate limit was reached.",
                suggestion="Wait a moment, then retry the lookup.",
                technical_detail=technical_detail,
                code="rate_limited",
            )
        if response.status_code >= 500:
            return NhvrToolsError(
                message="The NHVR registration service is unavailable right now.",
                suggestion="Try again later.",
                technical_detail=technical_detail,
                code="service_unavailable",
            )

        return NhvrToolsError(
            message=f"NHVR API request failed with status {response.status_code}.",
            suggestion="Try again later or check the request details.",
            technical_detail=technical_detail,
            code="api_error",
        )
