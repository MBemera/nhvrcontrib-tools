"""Interactive setup wizard for MCP users."""

from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

USE_COLOR = sys.stdout.isatty() and (os.name != "nt" or os.environ.get("WT_SESSION"))
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _color(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def green(text: str) -> str:
    return _color("32", text)


def yellow(text: str) -> str:
    return _color("33", text)


def red(text: str) -> str:
    return _color("31", text)


def bold(text: str) -> str:
    return _color("1", text)


def cyan(text: str) -> str:
    return _color("36", text)


def banner() -> None:
    print()
    print(bold("=" * 56))
    print(bold("   NHVR Tools Setup"))
    print(bold("   Claude Desktop / MCP Configuration"))
    print(bold("=" * 56))
    print()
    print("  This wizard configures the MCP server entry for Claude Desktop.")
    print("  Packaging is managed by pyproject.toml. Use `nhvr-setup`, not")
    print("  `python setup.py`, for the normal setup flow.")
    print()


def ask_yes_no(question: str, default: bool = True) -> bool:
    hint = "[Y/n]" if default else "[y/N]"
    while True:
        answer = input(f"  {question} {hint} ").strip().lower()
        if answer == "":
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print(f"  {yellow('Please type y or n.')}")


def ask_text(question: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    answer = input(f"  {question}{hint} ").strip()
    return answer or default


def step(number: int, title: str) -> None:
    print()
    print(f"  {bold(cyan(f'Step {number}'))}  {bold(title)}")
    print(f"  {'─' * 48}")


def ok(message: str) -> None:
    print(f"  {green('✓')} {message}")


def warn(message: str) -> None:
    print(f"  {yellow('!')} {message}")


def fail(message: str) -> None:
    print(f"  {red('✗')} {message}")


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
    )


def check_python() -> bool:
    step(1, "Checking Python version")
    version = sys.version_info
    version_text = f"{version.major}.{version.minor}.{version.micro}"
    if version >= (3, 10):
        ok(f"Python {version_text} is supported.")
        return True

    fail(f"Python {version_text} found, but 3.10+ is required.")
    print(f"  Install a newer version from {cyan('https://www.python.org/downloads/')}")
    return False


def ensure_mcp_dependencies() -> bool:
    step(2, "Checking MCP server dependencies")
    if module_is_available("fastmcp"):
        ok("The MCP server extra is already installed.")
        return True

    warn("The MCP server extra is not installed yet.")
    if is_source_checkout(PROJECT_ROOT):
        print("  This looks like a source checkout, so the wizard can install it.")
        if ask_yes_no("Install the MCP extra now?", default=True):
            result = run([sys.executable, "-m", "pip", "install", "-e", ".[mcp]"], cwd=PROJECT_ROOT)
            if result.returncode == 0:
                ok("Installed the MCP extra from source.")
                return True
            fail("Could not install the MCP extra automatically.")
            print_recent_stderr(result)
        print('  Run manually: ' + cyan('pip install -e ".[mcp]"'))
        return False

    print('  Install it first: ' + cyan('pip install "nhvr-tools[mcp]"'))
    return False


def configure_optional_scraper() -> None:
    step(3, "Optional live NHVR scraping")
    print(
        textwrap.indent(
            textwrap.dedent(
                """\
                Search and scrape commands can use Playwright for live NHVR pages.
                This is optional. Knowledge-base lookups, CLI help, and the MCP
                server startup all work without it.
                """
            ),
            "  ",
        )
    )

    if not module_is_available("playwright.async_api"):
        warn("Playwright is not installed.")
        print('  Install later with: ' + cyan('pip install "nhvr-tools[scraper]"'))
        print(f"  Then install the browser with: {cyan('playwright install chromium')}")
        return

    ok("Playwright is installed.")
    if ask_yes_no("Install the Chromium browser now?", default=False):
        result = run([sys.executable, "-m", "playwright", "install", "chromium"])
        if result.returncode == 0:
            ok("Chromium is installed.")
            return
        warn("Chromium could not be installed automatically.")
        print_recent_stderr(result)
        print(f"  Run later: {cyan('playwright install chromium')}")
        return

    warn("Skipped browser install.")


def configure_api_key() -> str | None:
    step(4, "Optional NHVR API key")
    print(
        textwrap.indent(
            textwrap.dedent(
                """\
                Registration lookups need an NHVR API key. If you do not have one,
                press Enter to skip this step. All static knowledge tools will still work.
                """
            ),
            "  ",
        )
    )

    api_key = ask_text("NHVR API key (or press Enter to skip):")
    if api_key:
        ok("The API key will be added to the MCP server environment.")
        return api_key

    warn("Skipped API key setup.")
    return None


def configure_claude_desktop(api_key: str | None) -> None:
    step(5, "Configuring Claude Desktop")

    config_path = get_claude_config_path()
    server_entry: dict[str, object] = {
        "command": sys.executable,
        "args": ["-m", "nhvr_mcp.server"],
    }
    if api_key:
        server_entry["env"] = {"NHVR_API_KEY": api_key}

    print(f"  Config file: {cyan(str(config_path))}")
    print()
    if not ask_yes_no("Write or update the Claude Desktop config now?", default=True):
        print_manual_config(server_entry, config_path)
        return

    config = read_config_file(config_path)
    config.setdefault("mcpServers", {})
    if "nhvr-tools" in config["mcpServers"]:
        overwrite_existing = ask_yes_no("An NHVR Tools entry already exists. Replace it?", default=False)
        if not overwrite_existing:
            ok("Kept the existing NHVR Tools entry.")
            return

    config["mcpServers"]["nhvr-tools"] = server_entry
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)
    ok("Claude Desktop config updated.")
    print(f"  {yellow('Restart Claude Desktop after setup.')}")


def test_server() -> bool:
    step(6, "Quick verification")
    import_result = run([sys.executable, "-c", "from nhvr_mcp.server import mcp; print('ok')"])
    if import_result.returncode == 0 and "ok" in import_result.stdout:
        ok("The MCP server module imports correctly.")
    else:
        fail("The MCP server module could not be imported.")
        print_recent_stderr(import_result)
        return False

    if module_is_available("click"):
        cli_result = run([sys.executable, "-m", "nhvr_mcp.cli", "--help"])
        if cli_result.returncode == 0:
            ok("The CLI is available.")
        else:
            warn("The CLI check failed. This is optional unless you installed the CLI extra.")
            print_recent_stderr(cli_result)
    else:
        warn("CLI extra not installed. Skip this check unless you need terminal commands.")

    return True


def finish() -> None:
    print()
    print(bold("=" * 56))
    print(bold(green("   Setup complete")))
    print(bold("=" * 56))
    print()
    print("  Next steps:")
    print("  1. Restart Claude Desktop.")
    print(f"  2. Ask a question like {cyan('What are the BFM fatigue rules?')}")
    print('  3. Optional scraper support: ' + cyan('pip install "nhvr-tools[scraper]"'))
    print(f"     Then run: {cyan('playwright install chromium')}")
    print()


def get_claude_config_path() -> Path:
    system_name = platform.system()
    if system_name == "Darwin":
        return Path("~/Library/Application Support/Claude/claude_desktop_config.json").expanduser()
    if system_name == "Windows":
        appdata = os.environ.get("APPDATA", "")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    return Path("~/.config/Claude/claude_desktop_config.json").expanduser()


def read_config_file(config_path: Path) -> dict:
    if not config_path.exists():
        return {}

    try:
        with config_path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        backup_path = config_path.with_suffix(config_path.suffix + ".backup")
        try:
            shutil.copy2(config_path, backup_path)
            warn(f"Existing config could not be read. A backup was saved to {backup_path}.")
        except OSError:
            warn("Existing config could not be read. A backup could not be created.")
        return {}


def print_manual_config(server_entry: dict[str, object], config_path: Path) -> None:
    print()
    print("  Add this entry under `mcpServers` in your Claude Desktop config:")
    snippet = json.dumps({"nhvr-tools": server_entry}, indent=2)
    for line in snippet.splitlines():
        print(f"    {line}")
    print()
    print(f"  Config path: {cyan(str(config_path))}")


def module_is_available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def is_source_checkout(project_root: Path) -> bool:
    return (project_root / "pyproject.toml").exists()


def print_recent_stderr(result: subprocess.CompletedProcess[str]) -> None:
    stderr_lines = [line for line in result.stderr.strip().splitlines() if line]
    for line in stderr_lines[-5:]:
        print(f"    {line}")


def main() -> None:
    banner()
    if not check_python():
        raise SystemExit(1)
    if not ensure_mcp_dependencies():
        raise SystemExit(1)

    configure_optional_scraper()
    api_key = configure_api_key()
    configure_claude_desktop(api_key)
    test_server()
    finish()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(f"  {yellow('Setup cancelled. Run `nhvr-setup` again when ready.')}")
        raise SystemExit(130)
