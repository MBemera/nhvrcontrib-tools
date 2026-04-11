from click.testing import CliRunner

from nhvr_mcp.cli import cli


def test_cli_help_runs() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "fatigue" in result.output
    assert "rego" in result.output


def test_cli_fatigue_rules_command() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["fatigue", "rules"])

    assert result.exit_code == 0
    assert "Summary" in result.output
    assert "Provenance" in result.output
