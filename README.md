# NHVR Contrib Tools

> Python SDK, MCP server, and CLI for Australian heavy vehicle compliance data.

[![CI](https://github.com/MBemera/nhvrcontrib-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/MBemera/nhvrcontrib-tools/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

`nhvrcontrib-tools` gives you quick access to fatigue rules, mass limits, dimension limits, Chain of Responsibility duties, accreditation guidance, permits, breach categories, and NHVR registration lookups.

> This project is an independent community contribution. It is not published, operated, or endorsed by the NHVR.

> HVNL reform note: the NHVR's [HVNL reform implementation page](https://www.nhvr.gov.au/law-policies/hvnl-reform-implementation) says the amended HVNL is expected to commence in mid-2026. The NHVR's HVA transition FAQs say it is working towards **1 July 2026**, subject to ministerial approval. That transition also progressively replaces NHVAS with the Heavy Vehicle Accreditation (HVA) scheme.

The upcoming `v0.4.0` release uses:

- Distribution name: `nhvrcontrib-tools`
- Python import path: `nhvrcontrib`
- CLI commands: `nhvr`, `nhvr-setup`

## Quick Start

Choose the smallest install that matches your use case:

| Use case | Install command | First command to try |
| --- | --- | --- |
| Python SDK | `pip install nhvrcontrib-tools` | `python -c "from nhvrcontrib import NHVR; print(NHVR().fatigue_rules()['summary'])"` |
| CLI | `pip install "nhvrcontrib-tools[cli]"` | `nhvr fatigue rules` |
| Claude Desktop / MCP | `pip install "nhvrcontrib-tools[mcp]"` | `nhvr-setup` |
| Live NHVR page scraping | `pip install "nhvrcontrib-tools[scraper]"` | `playwright install chromium` |
| Everything | `pip install "nhvrcontrib-tools[all]"` | `nhvr --help` |

Playwright is optional. Base imports, SDK usage, CLI help, CLI knowledge commands, and MCP server startup work without it.

## Install

`nhvrcontrib-tools` is the package name for the renamed `v0.4.0` release. If that release is not yet on PyPI, install from source or from a local wheel.

### Install From Source

```bash
git clone https://github.com/MBemera/nhvrcontrib-tools.git
cd nhvrcontrib-tools
pip install -e ".[dev]"
```

For a smaller source install:

```bash
pip install -e .
pip install -e ".[cli]"
pip install -e ".[mcp]"
```

### Install From A Wheel

```bash
python -m build
pip install dist/nhvrcontrib_tools-0.4.0-py3-none-any.whl
```

### Optional Playwright Install

```bash
pip install "nhvrcontrib-tools[scraper]"
playwright install chromium
```

If Playwright is missing, scraper-specific commands return a readable install hint instead of crashing.

## Claude Desktop And MCP

### Recommended Setup

```bash
pip install "nhvrcontrib-tools[mcp]"
nhvr-setup
```

`nhvr-setup` checks the MCP dependency, offers optional Playwright guidance, stores the NHVR API key in your machine credential manager, writes the Claude Desktop config, and verifies that the server imports correctly.

Useful setup commands:

```bash
nhvr-setup --help
nhvr-setup --print-config
nhvr-setup --yes --api-key "your-nhvr-api-key"
```

`nhvr-setup` is safe in non-interactive shells. If there is no stdin, it prints the config snippet instead of crashing or silently overwriting files.

### Provenance And Currency

Every response is annotated so you can see where the content came from:

- Built-in knowledge tools return cached summaries that include `source_title`, `source_url`, `last_verified`, and `source_type: static_knowledge`. Markdown responses render a `Source:` footer with the verification date.
- Where a reliable HVNL anchor exists (for example, Chain of Responsibility primary duty at `sec.26C`), responses include a `section_reference` and a `deep_link_url` into the Queensland legislation view of the HVNL. Markdown output prefers the deep link.
- Live `nhvr_search_regulations` and `nhvr_scrape_page` responses include `source_type: live_scrape` and a `scraped_at` UTC timestamp so callers can tell when the page was fetched.
- When live scraping fails, the search tool returns a static fallback clearly flagged with `source_type: static_fallback` and a `fallback_reason`, and still surfaces the underlying provenance.

Treat cached responses as a quick orientation layer. Always verify operational, safety, or legal decisions against the current official NHVR and HVNL sources linked in the footer.

### Responsible Use

The built-in knowledge tools return cached summaries with provenance footers:

- `nhvr_get_fatigue_rules`
- `nhvr_get_mass_limits`
- `nhvr_get_dimension_limits`
- `nhvr_get_breach_categories`
- `nhvr_get_speed_limits`
- `nhvr_get_cor_duties`
- `nhvr_get_accreditation_info`
- `nhvr_get_permit_types`
- `nhvr_get_hml_info`

The live-access tools depend on current NHVR systems or live web content:

- `nhvr_search_vehicle_registration`
- `nhvr_search_regulations`
- `nhvr_scrape_page`

Access to the live endpoints should stay within the audience and use case your NHVR API key or operational approval was issued for. The registration endpoint is monitored and is intended for operator fleet management, not bulk extracts.

### Manual Claude Desktop Config

Claude Desktop config paths:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Use the same Python interpreter that has `nhvrcontrib-tools[mcp]` installed:

```json
{
  "mcpServers": {
    "nhvrcontrib-tools": {
      "command": "python3",
      "args": ["-m", "nhvrcontrib.server"]
    }
  }
}
```

Desktop registration lookups read the API key from the machine credential manager. For CI, Docker, or other non-desktop environments, keep using `NHVR_API_KEY`.

### Run The MCP Server Directly

```bash
# stdio transport
python -m nhvrcontrib.server

# HTTP transport
NHVR_MCP_TRANSPORT=streamable_http \
NHVR_MCP_HOST=0.0.0.0 \
NHVR_MCP_PORT=8080 \
python -m nhvrcontrib.server
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
| `nhvr_search_vehicle_registration` | Vehicle registration lookup. Monitored by NHVR. Intended for operator fleet management, not bulk extracts. |
| `nhvr_search_regulations` | Natural-language topic search with fallback suggestions |
| `nhvr_scrape_page` | Scrape a specific `nhvr.gov.au` page |

## CLI

Install:

```bash
pip install "nhvrcontrib-tools[cli]"
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

Static markdown responses end with a source footer, source type, section reference where available, and verification date. Live search and scrape responses add a scrape timestamp and a source-type line. JSON responses include the same provenance fields structurally.

## Python SDK

```python
from nhvrcontrib import NHVR

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
from nhvrcontrib import NHVR

client = NHVR()

rego = asyncio.run(client.search_registration("ABC123"))
search = asyncio.run(client.search("b-double mass"))
page = asyncio.run(client.scrape("https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits"))
```

`search_registration()` resolves credentials in this order:

1. `api_key=` passed to `NHVR(...)`
2. `NHVR_API_KEY` environment variable
3. System credential manager entry created by `nhvr-setup`

## Docker

The default image runs the MCP server with the `mcp` extra installed. It is intended for MCP clients, not for interactive CLI use.

Build the image:

```bash
docker build -t nhvrcontrib-tools .
```

### Run MCP Over Stdio

Use stdio mode when the container is attached directly to an MCP client process:

```bash
docker run --rm -i nhvrcontrib-tools
```

### Run MCP Over HTTP

```bash
docker run --rm \
  -p 8080:8080 \
  -e NHVR_MCP_TRANSPORT=streamable_http \
  -e NHVR_MCP_HOST=0.0.0.0 \
  -e NHVR_MCP_PORT=8080 \
  nhvrcontrib-tools
```

Then connect your MCP-capable client to port `8080`.

### Docker Environment Variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `NHVR_MCP_TRANSPORT` | MCP transport mode: `stdio` or `streamable_http` | `stdio` |
| `NHVR_MCP_HOST` | HTTP bind host | `0.0.0.0` |
| `NHVR_MCP_PORT` | HTTP port | `8080` |
| `NHVR_API_KEY` | Enables registration lookups in Docker and CI | unset |

### Docker Note About Scraping

The default image does not install Playwright. That keeps the container smaller and allows MCP startup without browser dependencies. Scraper-specific operations return a clear install hint instead of crashing.

If you need live NHVR scraping inside Docker, extend the image with:

```bash
pip install "nhvrcontrib-tools[scraper]"
playwright install chromium
```

You may also need the extra Playwright system packages required by your base image.

## Troubleshooting

### `nhvr-setup` printed config instead of writing it

That usually means the command ran without interactive stdin. Run `nhvr-setup` in a normal terminal, or use `nhvr-setup --yes` to accept default prompts explicitly.

### `ModuleNotFoundError: fastmcp`

Install the MCP extra:

```bash
pip install "nhvrcontrib-tools[mcp]"
```

### Scraper command says Playwright is required

Install scraper support and the browser:

```bash
pip install "nhvrcontrib-tools[scraper]"
playwright install chromium
```

### Registration lookup says an API key is required

For Docker, CI, or shell usage:

```bash
export NHVR_API_KEY="your-key"
```

For desktop usage:

```bash
nhvr-setup --api-key "your-key"
```

Or pass it directly in code:

```python
from nhvrcontrib import NHVR

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
git ls-files -z | xargs -0 detect-secrets-hook --baseline .secrets.baseline
pytest
python -m build
python -m twine check dist/*
```

## Data Sources

Built-in knowledge is based on official NHVR and HVNL material, including:

- [NHVR website](https://www.nhvr.gov.au/)
- [Heavy Vehicle National Law and regulations](https://www.nhvr.gov.au/law-policies/heavy-vehicle-national-law-and-regulations)
- [Queensland legislation view of the HVNL](https://www.legislation.qld.gov.au/view/whole/html/inforce/current/act-2012-hvnlq)
- [NHVR developer portal](https://api-portal.nhvr.gov.au/)

This repository remains unofficial. Always verify operational and legal requirements against current official sources.

## License

MIT
