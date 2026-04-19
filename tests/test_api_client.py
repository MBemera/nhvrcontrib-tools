from nhvrcontrib.api_client import NhvrApiClient


def test_api_client_prefers_explicit_key_over_env_and_keyring(monkeypatch) -> None:
    monkeypatch.setenv("NHVR_API_KEY", "env-key")
    monkeypatch.setattr("nhvrcontrib.api_client.get_keyring_api_key", lambda: "keyring-key")

    client = NhvrApiClient(api_key="explicit-key")

    assert client.api_key == "explicit-key"  # pragma: allowlist secret


def test_api_client_uses_env_before_keyring(monkeypatch) -> None:
    monkeypatch.setenv("NHVR_API_KEY", "env-key")
    monkeypatch.setattr("nhvrcontrib.api_client.get_keyring_api_key", lambda: "keyring-key")

    client = NhvrApiClient()

    assert client.api_key == "env-key"  # pragma: allowlist secret


def test_api_client_uses_keyring_when_env_missing(monkeypatch) -> None:
    monkeypatch.delenv("NHVR_API_KEY", raising=False)
    monkeypatch.setattr("nhvrcontrib.api_client.get_keyring_api_key", lambda: "keyring-key")

    client = NhvrApiClient()

    assert client.api_key == "keyring-key"  # pragma: allowlist secret
