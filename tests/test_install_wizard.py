from pathlib import Path

import pytest

from nhvr_mcp import install_wizard


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
    assert "Add this entry under `mcpServers`" in output
    assert not config_path.exists()


def test_main_print_config_uses_default_answers(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_path = tmp_path / "claude_desktop_config.json"

    monkeypatch.setattr(install_wizard, "check_python", lambda: True)
    monkeypatch.setattr(install_wizard, "ensure_mcp_dependencies", lambda prompts: True)
    monkeypatch.setattr(install_wizard, "configure_optional_scraper", lambda prompts: None)
    monkeypatch.setattr(install_wizard, "test_server", lambda: True)
    monkeypatch.setattr(install_wizard, "get_claude_config_path", lambda: config_path)

    exit_code = install_wizard.main(["--yes", "--print-config", "--api-key", "test-key"])

    assert exit_code == 0
    output = capsys.readouterr().out
    assert "Add this entry under `mcpServers`" in output
    assert '"NHVR_API_KEY": "test-key"' in output
    assert not config_path.exists()
