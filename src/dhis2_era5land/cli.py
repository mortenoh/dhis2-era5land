"""CLI for dhis2-era5land."""

import logging
from typing import Annotated

import typer
import uvicorn
from dhis2_client import DHIS2Client

from dhis2_era5land.importer import import_era5_land_to_dhis2
from dhis2_era5land.settings import settings
from dhis2_era5land.transforms import Transform, get_transform

app = typer.Typer(
    help="Import ERA5-Land climate data into DHIS2.",
    no_args_is_help=True,
)


@app.command()
def run(
    # Date range
    start_date: Annotated[str, typer.Option(help="Start date (YYYY-MM-DD)")] = settings.start_date,
    end_date: Annotated[str, typer.Option(help="End date (YYYY-MM-DD)")] = settings.end_date,
    # DHIS2 connection (password from env only)
    base_url: Annotated[str | None, typer.Option(help="DHIS2 base URL (required)")] = None,
    username: Annotated[str | None, typer.Option(help="DHIS2 username (required)")] = None,
    # ERA5 config
    variable: Annotated[str, typer.Option(help="ERA5 variable name")] = settings.variable,
    data_element_id: Annotated[str | None, typer.Option(help="DHIS2 data element ID (required)")] = None,
    value_col: Annotated[str, typer.Option(help="Value column name")] = settings.value_col,
    value_transform: Annotated[Transform, typer.Option(help="Value transform")] = settings.value_transform,
    # Aggregation
    temporal_aggregation: Annotated[
        str, typer.Option(help="Temporal aggregation (sum/mean)")
    ] = settings.temporal_aggregation,
    spatial_aggregation: Annotated[str, typer.Option(help="Spatial aggregation (mean)")] = settings.spatial_aggregation,
    # Other
    timezone_offset: Annotated[int, typer.Option(help="Timezone offset in hours")] = settings.timezone_offset,
    org_unit_level: Annotated[int, typer.Option(help="Org unit level")] = settings.org_unit_level,
    # Flags
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Don't actually import")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable debug logging")] = False,
) -> None:
    """Run the ERA5-Land to DHIS2 import."""
    # Validate all required options
    missing: list[str] = []
    if not base_url:
        missing.append("--base-url")
    if not username:
        missing.append("--username")
    if not settings.password:
        missing.append("DHIS2_PASSWORD (env)")
    if not data_element_id:
        missing.append("--data-element-id")
    if missing:
        raise typer.BadParameter(f"Missing required options: {', '.join(missing)}")

    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    # Create DHIS2 client (validated above)
    client = DHIS2Client(
        base_url=base_url,  # type: ignore[arg-type]
        username=username,  # type: ignore[arg-type]
        password=settings.password,  # type: ignore[arg-type]
    )

    # Get transform function by name
    value_func = get_transform(value_transform)

    import_era5_land_to_dhis2(
        client,
        variable=variable,
        data_element_id=data_element_id,  # type: ignore[arg-type]
        value_col=value_col,
        value_func=value_func,
        temporal_aggregation=temporal_aggregation,
        spatial_aggregation=spatial_aggregation,
        start_date=start_date,
        end_date=end_date,
        timezone_offset=timezone_offset,
        org_unit_level=org_unit_level,
        dry_run=dry_run,
    )


@app.command()
def serve(
    host: Annotated[str, typer.Option(help="Host to bind to")] = "0.0.0.0",
    port: Annotated[int, typer.Option(help="Port to listen on")] = 8080,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable debug logging")] = False,
) -> None:
    """Start the API server."""
    log_level = "debug" if verbose else "info"
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    uvicorn.run(
        "dhis2_era5land.server:app",
        host=host,
        port=port,
        log_level=log_level,
    )
