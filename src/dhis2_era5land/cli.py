"""CLI for dhis2-era5land."""

import logging
import os
from typing import Annotated

import typer
import uvicorn
from dhis2_client import DHIS2Client

from dhis2_era5land.importer import import_era5_land_to_dhis2
from dhis2_era5land.settings import cds_settings, settings
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
    base_url: Annotated[str, typer.Option(help="DHIS2 base URL")] = settings.base_url or ...,  # type: ignore[assignment]
    username: Annotated[str, typer.Option(help="DHIS2 username")] = settings.username or ...,  # type: ignore[assignment]
    # ERA5 config
    variable: Annotated[str, typer.Option(help="ERA5 variable name")] = settings.variable,
    data_element_id: Annotated[str, typer.Option(help="DHIS2 data element ID")] = settings.data_element_id or ...,  # type: ignore[assignment]
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
    # Validate required env vars
    if not settings.password:
        raise typer.BadParameter("DHIS2_PASSWORD environment variable is required")
    if not cds_settings.key:
        raise typer.BadParameter(
            "CDSAPI_KEY environment variable is required (get one from https://cds.climate.copernicus.eu/how-to-api)"
        )

    # Export CDS settings to environment for cdsapi library
    os.environ["CDSAPI_URL"] = cds_settings.url
    os.environ["CDSAPI_KEY"] = cds_settings.key

    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    # Create DHIS2 client
    client = DHIS2Client(
        base_url=base_url,
        username=username,
        password=settings.password,
    )

    # Get transform function by name
    value_func = get_transform(value_transform)

    import_era5_land_to_dhis2(
        client,
        variable=variable,
        data_element_id=data_element_id,
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
