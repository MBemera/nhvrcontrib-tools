"""CLI for NHVR tools."""

from __future__ import annotations

import asyncio
from typing import Any

import click

from nhvrcontrib.errors import is_error_response
from nhvrcontrib.formatters import format_response
from nhvrcontrib.service import (
    get_accreditation_info_data,
    get_breach_categories_data,
    get_cor_duties_data,
    get_dimension_limits_data,
    get_fatigue_rules_data,
    get_hml_info_data,
    get_mass_limits_data,
    get_permit_types_data,
    get_speed_limits_data,
    scrape_page_data,
    search_regulations_data,
    search_vehicle_registration_data,
)


def emit_response(data: dict[str, Any], output_format: str) -> None:
    click.echo(format_response(data, output_format))
    if is_error_response(data):
        raise click.exceptions.Exit(1)


@click.group()
@click.option("--format", "output_format", default="markdown", type=click.Choice(["markdown", "json"]))
@click.pass_context
def cli(context: click.Context, output_format: str) -> None:
    context.ensure_object(dict)
    context.obj["output_format"] = output_format


@cli.group()
def fatigue() -> None:
    """Fatigue rules."""


@fatigue.command("rules")
@click.option("--scheme", default="standard", type=click.Choice(["standard", "bfm", "afm"]))
@click.pass_context
def fatigue_rules(context: click.Context, scheme: str) -> None:
    """Show fatigue rules for a work and rest scheme."""
    output_format = context.obj["output_format"]
    emit_response(get_fatigue_rules_data(scheme=scheme), output_format)


@cli.group()
def mass() -> None:
    """Mass limits."""


@mass.command("limits")
@click.option("--include-hml", is_flag=True, default=False)
@click.pass_context
def mass_limits(context: click.Context, include_hml: bool) -> None:
    """Show general mass limits and optional HML data."""
    output_format = context.obj["output_format"]
    emit_response(get_mass_limits_data(include_hml=include_hml), output_format)


@mass.command("hml")
@click.pass_context
def mass_hml(context: click.Context) -> None:
    """Show Higher Mass Limits guidance."""
    output_format = context.obj["output_format"]
    emit_response(get_hml_info_data(), output_format)


@cli.group()
def dimension() -> None:
    """Dimension limits."""


@dimension.command("limits")
@click.pass_context
def dimension_limits(context: click.Context) -> None:
    """Show heavy vehicle dimension limits."""
    output_format = context.obj["output_format"]
    emit_response(get_dimension_limits_data(), output_format)


@cli.group()
def breach() -> None:
    """Breach categories."""


@breach.command("categories")
@click.option("--type", "breach_type", default=None)
@click.pass_context
def breach_categories(context: click.Context, breach_type: str | None) -> None:
    """Show breach categories for one type or all types."""
    output_format = context.obj["output_format"]
    emit_response(get_breach_categories_data(breach_type=breach_type), output_format)


@cli.command("speed")
@click.pass_context
def speed_limits(context: click.Context) -> None:
    """Show heavy vehicle speed limits and limiter rules."""
    output_format = context.obj["output_format"]
    emit_response(get_speed_limits_data(), output_format)


@cli.group()
def cor() -> None:
    """Chain of Responsibility duties."""


@cor.command("duties")
@click.option("--role", default=None)
@click.pass_context
def cor_duties(context: click.Context, role: str | None) -> None:
    """Show Chain of Responsibility duties by role."""
    output_format = context.obj["output_format"]
    emit_response(get_cor_duties_data(role=role), output_format)


@cli.command("accreditation")
@click.option("--module", default=None)
@click.pass_context
def accreditation(context: click.Context, module: str | None) -> None:
    """Show NHVAS accreditation guidance."""
    output_format = context.obj["output_format"]
    emit_response(get_accreditation_info_data(module=module), output_format)


@cli.command("permits")
@click.option("--type", "permit_type", default=None)
@click.pass_context
def permits(context: click.Context, permit_type: str | None) -> None:
    """Show access permit guidance."""
    output_format = context.obj["output_format"]
    emit_response(get_permit_types_data(permit_type=permit_type), output_format)


@cli.command("rego")
@click.argument("plate_number")
@click.pass_context
def rego(context: click.Context, plate_number: str) -> None:
    """Look up a vehicle registration by plate number."""
    output_format = context.obj["output_format"]
    result = asyncio.run(search_vehicle_registration_data(plate_number=plate_number))
    emit_response(result, output_format)


@cli.command("search")
@click.argument("query")
@click.pass_context
def search(context: click.Context, query: str) -> None:
    """Search NHVR topics with live scraping and static fallback."""
    output_format = context.obj["output_format"]
    result = asyncio.run(search_regulations_data(query=query))
    emit_response(result, output_format)


@cli.command("scrape")
@click.argument("url")
@click.pass_context
def scrape(context: click.Context, url: str) -> None:
    """Scrape a specific NHVR page."""
    output_format = context.obj["output_format"]
    result = asyncio.run(scrape_page_data(url=url))
    emit_response(result, output_format)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
