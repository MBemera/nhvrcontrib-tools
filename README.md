# NHVR Tools

> Python SDK, MCP server, and CLI for Australian heavy vehicle compliance data.

[![PyPI version](https://img.shields.io/pypi/v/nhvr-tools?cacheSeconds=60)](https://pypi.org/project/nhvr-tools/)
[![PyPI downloads](https://img.shields.io/pypi/dm/nhvr-tools?cacheSeconds=60)](https://pypi.org/project/nhvr-tools/)
[![Python](https://img.shields.io/pypi/pyversions/nhvr-tools?cacheSeconds=60)](https://pypi.org/project/nhvr-tools/)
[![CI](https://github.com/MBemera/nhvr-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/MBemera/nhvr-tools/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

`nhvr-tools` gives you quick access to fatigue rules, mass limits, dimension limits, Chain of Responsibility duties, accreditation guidance, permits, breach categories, and NHVR registration lookups.

The PyPI package name is `nhvr-tools`. The Python import path is `nhvr_mcp`.

## Quick Start

Choose the smallest install that matches your use case:

| Use case | Install command | First command to try |
| --- | --- | --- |
| Python SDK | `pip install nhvr-tools` | `python -c "from nhvr_mcp import NHVR; print(NHVR().fatigue_rules()['summary'])"` |
| CLI | `pip install "nhvr-tools[cli]"` | `nhvr fatigue rules` |
| Claude Desktop / MCP | `pip install "nhvr-tools[mcp]"` | `nhvr-setup` |
| Live NHVR page scraping | `pip install "nhvr-tools[scraper]"` | `playwright install chromium` |
| Everything | `pip install "nhvr-tools[all]"` | `nhvr --help` |

Playwright is optional. Base imports, SDK usage, CLI help, CLI knowledge commands, and MCP server startup work without it.

## Install

### Install From PyPI

```bash
pip install nhvr-tools
pip install "nhvr-tools[cli]"
pip install "nhvr-tools[mcp]"
pip install "nhvr-tools[all]"
```

### Install From Source

```bash
git clone https://github.com/MBemera/nhvr-tools.git
cd nhvr-tools
pip install -e ".[dev]"
```

For a smaller source install:

```bash
pip install -e .
pip install -e ".[cli]"
pip install -e ".[mcp]"
```

### Optional Playwright Install

```bash
pip install "nhvr-tools[scraper]"
playwright install chromium
```

If Playwright is missing, scraper-specific commands return a readable install hint instead of crashing.

## Claude Desktop And MCP

### Recommended Setup

```bash
pip install "nhvr-tools[mcp]"
nhvr-setup
```

`nhvr-setup` checks the MCP dependency, offers optional API key and Playwright guidance, writes the Claude Desktop config, and verifies that the server imports correctly.

Useful setup commands:

```bash
nhvr-setup --help
nhvr-setup --print-config
nhvr-setup --yes --api-key "your-nhvr-api-key"
```

`nhvr-setup` is safe in non-interactive shells. If there is no stdin, it prints the config snippet instead of crashing or silently overwriting files.

### Manual Claude Desktop Config

Claude Desktop config paths:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Use the same Python interpreter that has `nhvr-tools[mcp]` installed:

```json
{
  "mcpServers": {
    "nhvr-tools": {
      "command": "python3",
      "args": ["-m", "nhvr_mcp.server"]
    }
  }
}
```

If you use registration lookups, add `NHVR_API_KEY` to the `env` block.

### Run The MCP Server Directly

```bash
# stdio transport
python -m nhvr_mcp.server

# HTTP transport
NHVR_MCP_TRANSPORT=streamable_http \
NHVR_MCP_HOST=0.0.0.0 \
NHVR_MCP_PORT=8080 \
python -m nhvr_mcp.server
```

### Available MCP Tools

| Tool | Description |
| --- | --- |
| `nhvr_get_fatigue_rules` | Work and rest hour requirements by scheme |
| `nhvr_get_mass_limits` | General and HML mass limits |
| `nhvr_get_dimension_limits` | Vehicle dimension limits |
| `nhvr_get_breach_categories` | Breach severity categories |
| `nhvr_get_speed_limits` | Speed limits and speed limiter rules |
| `nhvr_get_cor_duties` | Chain of Responsibility duties |
| `nhvr_get_accreditation_info` | NHVAS and HVA guidance |
| `nhvr_get_permit_types` | Access permit types |
| `nhvr_get_hml_info` | Higher Mass Limits guidance |
| `nhvr_search_vehicle_registration` | Vehicle registration lookup |
| `nhvr_search_regulations` | Natural-language topic search with fallback suggestions |
| `nhvr_scrape_page` | Scrape a specific `nhvr.gov.au` page |

## CLI

Install:

```bash
pip install "nhvr-tools[cli]"
```

Common commands:

```bash
nhvr fatigue rules
nhvr fatigue rules --scheme bfm
nhvr mass limits --include-hml
nhvr mass hml
nhvr dimension limits
nhvr breach categories --type mass
nhvr cor duties --role operator
nhvr accreditation --module fatigue
nhvr permits --type oversize
nhvr rego ABC123
nhvr search "rest breaks"
nhvr --format json fatigue rules
```

Search uses aliases and lightweight fuzzy matching. Queries like `bfm`, `afm`, `rest breaks`, `b-double mass`, `loader duty`, `executive due diligence`, `speed limiter`, and `oversize permits` resolve more reliably than plain substring matching. If there is no strong match, the CLI suggests likely topics instead of returning a dead end.

## Python SDK

```python
from nhvr_mcp import NHVR

client = NHVR()

fatigue = client.fatigue_rules("bfm")
mass = client.mass_limits(include_hml=True)
dimensions = client.dimension_limits()
cor = client.cor_duties("operator")
permits = client.permit_types("oversize")
```

Async methods:

```python
import asyncio
from nhvr_mcp import NHVR

client = NHVR(api_key="your-nhvr-api-key")

rego = asyncio.run(client.search_registration("ABC123"))
search = asyncio.run(client.search("b-double mass"))
page = asyncio.run(client.scrape("https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits"))
```

`search_registration()` needs an NHVR API key. `search()` and `scrape()` may use Playwright for live NHVR pages. If live scraping is unavailable, topic search falls back to the built-in knowledge base where possible.

Static knowledge responses include:

- `source_title`
- `source_url`
- `last_verified`
- `unofficial_warning`

## Docker

The default image runs the MCP server with the `mcp` extra installed. It is intended for MCP clients, not for interactive CLI use.

Build the image:

```bash
docker build -t nhvr-tools .
```

### Run MCP Over Stdio

Use stdio mode when the container is attached directly to an MCP client process:

```bash
docker run --rm -i nhvr-tools
```

### Run MCP Over HTTP

```bash
docker run --rm \
  -p 8080:8080 \
  -e NHVR_MCP_TRANSPORT=streamable_http \
  -e NHVR_MCP_HOST=0.0.0.0 \
  -e NHVR_MCP_PORT=8080 \
  nhvr-tools
```

Then connect your MCP-capable client to port `8080`.

### Docker Environment Variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `NHVR_MCP_TRANSPORT` | MCP transport mode: `stdio` or `streamable_http` | `stdio` |
| `NHVR_MCP_HOST` | HTTP bind host | `0.0.0.0` |
| `NHVR_MCP_PORT` | HTTP port | `8080` |
| `NHVR_API_KEY` | Enables registration lookups | unset |

### Docker Note About Scraping

The default image does not install Playwright. That keeps the container smaller and allows MCP startup without browser dependencies. Scraper-specific operations return a clear install hint instead of crashing.

If you need live NHVR scraping inside Docker, extend the image with:

```bash
pip install "nhvr-tools[scraper]"
playwright install chromium
```

You may also need the extra Playwright system packages required by your base image.

## Troubleshooting

### `nhvr-setup` printed config instead of writing it

That usually means the command ran without interactive stdin. Run `nhvr-setup` in a normal terminal, or use `nhvr-setup --yes` to accept default prompts explicitly.

### `ModuleNotFoundError: fastmcp`

Install the MCP extra:

```bash
pip install "nhvr-tools[mcp]"
```

### Scraper command says Playwright is required

Install scraper support and the browser:

```bash
pip install "nhvr-tools[scraper]"
playwright install chromium
```

### Registration lookup says an API key is required

Set the environment variable or pass it directly:

```bash
export NHVR_API_KEY="your-key"
```

```python
from nhvr_mcp import NHVR

client = NHVR(api_key="your-key")
```

### Search could not find a topic

Use one of the suggested topics, or scrape a specific NHVR page directly:

```bash
nhvr scrape "https://www.nhvr.gov.au/road-access/access-permits"
```

## Development

Install the dev environment:

```bash
pip install -e ".[dev]"
```

Run the local checks:

```bash
ruff check .
pytest
python -m build
python -m twine check dist/*
```

## Data Sources

Built-in knowledge is based on official NHVR and HVNL material, including:

- [NHVR website](https://www.nhvr.gov.au/)
- [Heavy Vehicle National Law and regulations](https://www.nhvr.gov.au/law-policies/heavy-vehicle-national-law-and-regulations)
- [NHVR developer portal](https://api-portal.nhvr.gov.au/)

This project is **unofficial**. It is not affiliated with or endorsed by the NHVR. Always verify operational and legal requirements against current official sources.

## License

MIT
