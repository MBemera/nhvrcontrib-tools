# NHVR Tools

> Python SDK, MCP server, and CLI for Australian heavy vehicle compliance data.

[![PyPI version](https://img.shields.io/pypi/v/nhvr-tools?cacheSeconds=60)](https://pypi.org/project/nhvr-tools/)
[![PyPI downloads](https://img.shields.io/pypi/dm/nhvr-tools?cacheSeconds=60)](https://pypi.org/project/nhvr-tools/)
[![Python](https://img.shields.io/pypi/pyversions/nhvr-tools?cacheSeconds=60)](https://pypi.org/project/nhvr-tools/)
[![CI](https://github.com/MBemera/nhvr-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/MBemera/nhvr-tools/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

`nhvr-tools` gives you quick access to fatigue rules, mass limits, dimension limits, chain of responsibility duties, accreditation guidance, permits, breach categories, and NHVR registration lookups.

The PyPI package name is `nhvr-tools`. The Python import path is `nhvr_mcp`.

## Choose Your Install Path

| Use case | Install command |
| --- | --- |
| Python SDK only | `pip install nhvr-tools` |
| CLI | `pip install "nhvr-tools[cli]"` |
| MCP server for Claude/Desktop clients | `pip install "nhvr-tools[mcp]"` |
| Live NHVR page scraping | `pip install "nhvr-tools[scraper]"` |
| Everything | `pip install "nhvr-tools[all]"` |

## Install From PyPI

```bash
# SDK only
pip install nhvr-tools

# CLI
pip install "nhvr-tools[cli]"

# MCP server
pip install "nhvr-tools[mcp]"

# Full install
pip install "nhvr-tools[all]"
```

### Optional Playwright Install

Playwright is only needed for live NHVR page scraping. Base imports, SDK usage, CLI help, knowledge-base commands, and MCP server startup do not require it.

```bash
pip install "nhvr-tools[scraper]"
playwright install chromium
```

If Playwright is missing, scraper-specific features fail with a readable message and install hint.

## Install From Source

```bash
git clone https://github.com/MBemera/nhvr-tools.git
cd nhvr-tools

# Pick the extra you need
pip install -e ".[mcp]"
pip install -e ".[cli]"
pip install -e ".[dev]"
```

## MCP Setup For Claude Desktop

Recommended path:

```bash
pip install "nhvr-tools[mcp]"
nhvr-setup
```

`nhvr-setup` checks the MCP dependency, offers optional API key and Playwright guidance, writes the Claude Desktop config, and verifies that the server imports correctly.

### Manual Claude Desktop Config

Add this to your Claude Desktop config:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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

If you use registration lookups, add `NHVR_API_KEY` to the server `env` block.

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
| `nhvr_get_accreditation_info` | NHVAS accreditation information |
| `nhvr_get_permit_types` | Access permit types |
| `nhvr_get_hml_info` | Higher Mass Limits guidance |
| `nhvr_search_vehicle_registration` | Vehicle registration lookup |
| `nhvr_search_regulations` | Natural-language topic search with fallback suggestions |
| `nhvr_scrape_page` | Scrape a specific `nhvr.gov.au` page |

## CLI

```bash
pip install "nhvr-tools[cli]"
```

```bash
nhvr fatigue rules
nhvr fatigue rules --scheme bfm
nhvr mass limits --include-hml
nhvr mass hml
nhvr dimension limits
nhvr breach categories --type mass
nhvr speed
nhvr cor duties --role operator
nhvr accreditation --module fatigue
nhvr permits --type oversize
nhvr rego ABC123
nhvr search "rest breaks"
nhvr scrape "https://www.nhvr.gov.au/road-access/access-permits"
nhvr --format json fatigue rules
```

Search now uses alias and fuzzy topic matching. Queries like `bfm`, `afm`, `rest breaks`, `b-double mass`, `executive due diligence`, `speed limiter`, and `oversize permits` map more reliably to relevant NHVR topics. If there is no strong match, the CLI returns a few likely topics instead of a dead end.

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

Static knowledge responses include provenance metadata:

- `source_title`
- `source_url`
- `last_verified`
- `unofficial_warning`

### Async SDK Methods

```python
import asyncio
from nhvr_mcp import NHVR

client = NHVR(api_key="your-nhvr-api-key")

rego = asyncio.run(client.search_registration("ABC123"))
search = asyncio.run(client.search("b-double mass"))
page = asyncio.run(client.scrape("https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits"))
```

`search_registration()` needs an NHVR API key. `search()` and `scrape()` may use Playwright for live NHVR pages. If live scraping is unavailable, topic search falls back to the built-in knowledge base where possible.

## Docker

The default image runs the MCP server with the `mcp` extra installed. It is intended for MCP clients, not for interactive CLI use.

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

Then connect to port `8080` from your MCP-capable client or reverse proxy.

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

You may also need the additional Playwright system packages required by your base image.

## Troubleshooting

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

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

## Data Sources

Built-in knowledge is based on official NHVR and HVNL material, including:

- [NHVR website](https://www.nhvr.gov.au/)
- [Heavy Vehicle National Law and regulations](https://www.nhvr.gov.au/law-policies/heavy-vehicle-national-law-and-regulations)
- [NHVR developer portal](https://api-portal.nhvr.gov.au/)

This project is **unofficial**. It is not affiliated with or endorsed by the NHVR. Always verify operational and legal requirements against current official sources.

## License

MIT
