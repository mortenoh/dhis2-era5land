"""CLI for dhis2-era5land."""

import logging

import typer
from dhis2_client import DHIS2Client

from dhis2_era5land.importer import import_era5_land_to_dhis2
from dhis2_era5land.settings import settings
from dhis2_era5land.transforms import get_transform

app = typer.Typer(help="Import ERA5-Land climate data into DHIS2.")


@app.command()
def run() -> None:
    """Run the ERA5-Land to DHIS2 import."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Create DHIS2 client from settings
    client = DHIS2Client(
        base_url=settings.base_url,
        username=settings.username,
        password=settings.password,
    )

    # Get transform function by name
    value_func = get_transform(settings.value_transform)

    import_era5_land_to_dhis2(
        client,
        variable=settings.variable,
        data_element_id=settings.data_element_id,
        value_col=settings.value_col,
        value_func=value_func,
        temporal_aggregation=settings.temporal_aggregation,
        spatial_aggregation=settings.spatial_aggregation,
        start_date=settings.start_date,
        end_date=settings.end_date,
        timezone_offset=settings.timezone_offset,
        org_unit_level=settings.org_unit_level,
    )
