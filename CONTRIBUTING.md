# Contributing to NHVR Contrib Tools

## Local Setup

```bash
git clone https://github.com/MBemera/nhvrcontrib-tools.git
cd nhvrcontrib-tools
pip install -e ".[dev]"
```

If you only need one profile:

```bash
pip install -e .
pip install -e ".[cli]"
pip install -e ".[mcp]"
```

## Before You Open A PR

Run the same checks the repo now expects locally:

```bash
ruff check .
pytest
python -m build
python -m twine check dist/*
```

If you touch setup, packaging, CLI entry points, or install docs, also smoke test the built artifact:

```bash
python -m venv .package-smoke
.package-smoke/bin/pip install dist/*.whl click fastmcp "pydantic>=2.0"
.package-smoke/bin/nhvr --help
.package-smoke/bin/nhvr-setup --help
```

## Making Changes

1. Branch from `main`.
2. Keep the public API stable unless a change is clearly justified.
3. Add or update tests with the code change.
4. Update `README.md`, `CHANGELOG.md`, and any affected docs when user-facing behavior changes.
5. Keep built-in knowledge summaries tied to official NHVR sources and provenance fields.

## Updating The Knowledge Base

The built-in data in `nhvrcontrib/knowledge.py` is sourced from the NHVR website and HVNL material.

When updating it:

- keep the existing data shape stable where practical
- include or update provenance fields such as `source_url`, `source_title`, and `last_verified`
- add or update tests that cover the changed topic
- repeat the manual verification flow documented in [SOURCE-VERIFICATION.md](SOURCE-VERIFICATION.md) when the legal summary changes

## Reporting Issues

Include:

- what you expected to happen
- what actually happened
- the command, prompt, or API call you used
- steps to reproduce
- Python version and OS
