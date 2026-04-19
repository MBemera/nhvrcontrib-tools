"""Credential helpers for NHVR API access."""

from __future__ import annotations

try:
    import keyring
    from keyring.errors import KeyringError
except ModuleNotFoundError:  # pragma: no cover - depends on the local install state
    keyring = None

    class KeyringError(Exception):
        """Fallback error used when keyring is unavailable."""


KEYRING_SERVICE_NAME = "nhvrcontrib-tools"
KEYRING_USERNAME = "nhvr_api_key"


def get_keyring_api_key() -> str | None:
    if keyring is None:
        return None

    try:
        return keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME)
    except KeyringError:
        return None


def store_keyring_api_key(api_key: str) -> bool:
    if keyring is None:
        return False

    try:
        keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME, api_key)
    except KeyringError:
        return False

    return True
