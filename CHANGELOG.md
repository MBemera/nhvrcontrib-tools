# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-04-13

### Changed

- Moved the user-facing setup flow to the installed `nhvr-setup` wizard and converted `setup.py` into a compatibility shim
- Hardened `nhvr-setup` so `--help`, `--print-config`, `--yes`, and non-interactive shells behave predictably without `EOFError`
- Clarified install paths for SDK, CLI, MCP, source installs, Playwright, and Docker usage
- Reworked README and contributor docs around task-based install, setup, Docker, troubleshooting, and release verification flows
- Improved search matching with aliases, fuzzy suggestions, and static fallback responses when live scraping is unavailable
- Added clearer user-facing API and scraper error messages for missing API keys, invalid plates, auth failures, timeouts, unavailable services, and missing Playwright
- Improved markdown response formatting for terminal and assistant output
- Added provenance metadata to static knowledge responses
- Manually re-verified static knowledge against live official NHVR guidance on 2026-04-11 and corrected fatigue, HML, dimension, accreditation, and permit summaries
- Updated Docker defaults so the image installs the MCP extra and can start the server reliably
- Expanded automated test coverage for CLI, search, formatter, and graceful failure paths
- Added CI packaging smoke checks for built artifacts and switched pytest to `importlib` mode with explicit project `pythonpath`

## [0.2.0] - 2025-03-09

### Fixed

- Scraper bot detection — Playwright now uses real browser user agent, viewport, and anti-detection settings
- HTTP fallback scraper now sends proper browser headers
- All 12 SDK methods fully functional including `search()` and `scrape()`

### Changed

- Minimal base dependencies (httpx, beautifulsoup4 only) — MCP, CLI, and scraper are optional extras
- Improved README with install badges, CI status, and PyPI links

## [0.1.0] - 2025-03-09

### Added

- Python SDK (`NHVR` client class) with sync and async methods
- MCP server with 12 tools for AI assistant integration
- CLI with full command coverage
- Built-in knowledge base: fatigue rules, mass limits, dimension limits, breach categories, speed limits, chain of responsibility, accreditation, permit types, HML info
- Vehicle registration lookup via NHVR public API
- NHVR website scraper with topic-specific parsers
- Setup wizard for non-technical users
- Docker support
