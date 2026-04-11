"""User-facing error helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class NhvrToolsError(Exception):
    """Expected error with a readable message and optional action."""

    message: str
    suggestion: str | None = None
    technical_detail: str | None = None
    code: str | None = None

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> dict[str, Any]:
        error: dict[str, Any] = {"message": self.message}
        if self.code:
            error["code"] = self.code
        if self.suggestion:
            error["suggestion"] = self.suggestion
        if self.technical_detail:
            error["technical_detail"] = self.technical_detail
        return {"error": error}


def as_error_response(error: Exception, default_message: str) -> dict[str, Any]:
    """Convert exceptions into a stable response payload."""

    if isinstance(error, NhvrToolsError):
        return error.to_dict()

    technical_detail = str(error).strip() or None
    return NhvrToolsError(
        message=default_message,
        technical_detail=technical_detail,
    ).to_dict()


def is_error_response(data: Any) -> bool:
    """Return True when the payload uses the standard error envelope."""

    return isinstance(data, dict) and isinstance(data.get("error"), dict)
