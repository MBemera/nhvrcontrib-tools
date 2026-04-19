import json
from pathlib import Path

import pytest

from nhvrcontrib import install_wizard


class StubPromptSession:
    def __init__(self, answers: list[bool]) -> None:
        self.answers = answers

    def confirm(self, question: str, default: bool = True, safe_default: bool | None = None) -> bool:
        if not self.answers:
            raise AssertionError(f"Unexpected prompt: {question}")
        return self.answers.pop(0)


def test_module_is_available_returns_false_for_missing_dotted_module() -> None:
    assert install_wizard.module_is_available("definitely_missing.module") is False


def test_parse_args_help_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        install_wizard.parse_args(["--help"])

    assert exc_info.value.code == 0
    output = capsys.readouterr().out
    assert "usage: nhvr-setup" in output
    assert "--print-config" in output


def test_main_non_interactive_prints_manual_config(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_path = tmp_path / "claude_desktop_config.json"

    monkeypatch.setattr(install_wizard, "input_is_interactive", lambda: False)
    monkeypatch.setattr(install_wizard, "check_python", lambda: True)
    monkeypatch.setattr(install_wizard, "ensure_mcp_dependencies", lambda prompts: True)
    monkeypatch.setattr(install_wizard, "configure_optional_scraper", lambda prompts: None)
    monkeypatch.setattr(install_wizard, "test_server", lambda: True)
    monkeypatch.setattr(install_wizard, "get_claude_config_path", lambda: config_path)

    exit_code = install_wizard.main([])

    assert exit_code == 0
    output = capsys.readouterr().out
    assert "No interactive input detected" in output
    assert '"nhvrcontrib-tools"' in output
    assert '"nhvr_mcp"' not in output
    assert not config_path.exists()


def test_main_print_config_stores_keyring_key_and_prints_secret_free_config(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_path = tmp_path / "claude_desktop_config.json"
    stored_keys: list[str] = []

    monkeypatch.setattr(install_wizard, "check_python", lambda: True)
    monkeypatch.setattr(install_wizard, "ensure_mcp_dependencies", lambda prompts: True)
    monkeypatch.setattr(install_wizard, "configure_optional_scraper", lambda prompts: None)
    monkeypatch.setattr(install_wizard, "test_server", lambda: True)
    monkeypatch.setattr(install_wizard, "get_claude_config_path", lambda: config_path)
    monkeypatch.setattr(
        install_wizard,
        "store_keyring_api_key",
        lambda api_key: stored_keys.append(api_key) or True,
    )

    exit_code = install_wizard.main(["--yes", "--print-config", "--api-key", "test-key"])

    assert exit_code == 0
    output = capsys.readouterr().out
    assert stored_keys == ["test-key"]
    assert '"nhvrcontrib-tools"' in output
    assert "NHVR_API_KEY" not in output
    assert not config_path.exists()


@pytest.mark.parametrize("invalid_json_value", [[], "value", 123])
def test_read_config_file_returns_empty_dict_for_non_object_json(
    tmp_path: Path,
    invalid_json_value: object,
) -> None:
    config_path = tmp_path / "claude_desktop_config.json"
    config_path.write_text(json.dumps(invalid_json_value), encoding="utf-8")

    result = install_wizard.read_config_file(config_path)

    assert result == {}
    backup_path = config_path.with_suffix(".json.backup")
    assert backup_path.exists()
    assert backup_path.read_text(encoding="utf-8") == json.dumps(invalid_json_value)


def test_print_manual_config_uses_renamed_server_entry(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    config_path = tmp_path / "claude_desktop_config.json"

    install_wizard.print_manual_config(install_wizard.build_server_entry(), config_path)

    output = capsys.readouterr().out
    assert '"nhvrcontrib-tools"' in output
    assert '"args"' in output
    assert '"nhvrcontrib.server"' in output
    assert "NHVR_API_KEY" not in output


def test_configure_claude_desktop_uses_atomic_write_and_migrates_plaintext_api_key(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "claude_desktop_config.json"
    existing_config = {
        "mcpServers": {
            "nhvr-tools": {
                "command": "python3",
                "args": ["-m", "old.server"],
                "env": {"NHVR_API_KEY": "super-secret-key"},
            },
            "existing-server": {"command": "python3", "args": ["-m", "existing.server"]},
        }
    }
    config_path.write_text(json.dumps(existing_config), encoding="utf-8")

    replace_calls: list[tuple[Path, Path]] = []
    stored_keys: list[str] = []
    real_replace = install_wizard.os.replace

    def tracking_replace(source: str | Path, destination: str | Path) -> None:
        replace_calls.append((Path(source), Path(destination)))
        real_replace(source, destination)

    monkeypatch.setattr(install_wizard, "get_claude_config_path", lambda: config_path)
    monkeypatch.setattr(
        install_wizard,
        "store_keyring_api_key",
        lambda api_key: stored_keys.append(api_key) or True,
    )
    monkeypatch.setattr(install_wizard.os, "replace", tracking_replace)

    prompts = StubPromptSession([True, True])
    install_wizard.configure_claude_desktop(prompts)

    temp_path = config_path.with_name(f"{config_path.name}.tmp")
    backup_path = config_path.with_suffix(".json.backup")

    assert stored_keys == ["super-secret-key"]
    assert replace_calls == [(temp_path, config_path)]
    assert not temp_path.exists()
    assert backup_path.exists()
    assert json.loads(backup_path.read_text(encoding="utf-8")) == existing_config

    written_config = json.loads(config_path.read_text(encoding="utf-8"))
    assert "nhvr-tools" not in written_config["mcpServers"]
    assert written_config["mcpServers"]["nhvrcontrib-tools"]["args"] == ["-m", "nhvrcontrib.server"]
    assert "env" not in written_config["mcpServers"]["nhvrcontrib-tools"]
    assert written_config["mcpServers"]["existing-server"]["args"] == ["-m", "existing.server"]


def test_configure_claude_desktop_keeps_existing_config_when_key_migration_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "claude_desktop_config.json"
    existing_config = {
        "mcpServers": {
            "nhvr-tools": {
                "command": "python3",
                "args": ["-m", "old.server"],
                "env": {"NHVR_API_KEY": "super-secret-key"},
            }
        }
    }
    config_path.write_text(json.dumps(existing_config), encoding="utf-8")

    monkeypatch.setattr(install_wizard, "get_claude_config_path", lambda: config_path)
    monkeypatch.setattr(install_wizard, "store_keyring_api_key", lambda api_key: False)

    prompts = StubPromptSession([True])
    install_wizard.configure_claude_desktop(prompts)

    assert json.loads(config_path.read_text(encoding="utf-8")) == existing_config
    assert not config_path.with_suffix(".json.backup").exists()
