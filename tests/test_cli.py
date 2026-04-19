from click.testing import CliRunner

from nhvrcontrib.cli import cli


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
    assert "_Source: [" in result.output


def test_cli_invalid_breach_type_returns_nonzero() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["breach", "categories", "--type", "bogus"])

    assert result.exit_code == 1
    assert "Unknown breach type" in result.output


def test_cli_invalid_permit_type_returns_nonzero() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["permits", "--type", "bogus"])

    assert result.exit_code == 1
    assert "Unknown permit type" in result.output


def test_cli_leaf_help_includes_command_description() -> None:
    runner = CliRunner()

    fatigue_help = runner.invoke(cli, ["fatigue", "rules", "--help"])
    search_help = runner.invoke(cli, ["search", "--help"])

    assert fatigue_help.exit_code == 0
    assert "Show fatigue rules for a work and rest scheme." in fatigue_help.output
    assert search_help.exit_code == 0
    assert "Search NHVR topics with live scraping and static fallback." in search_help.output
