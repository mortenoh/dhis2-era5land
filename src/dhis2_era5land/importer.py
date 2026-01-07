"""ERA5-Land to DHIS2 import functionality."""

import json
import logging
from collections.abc import Callable
from datetime import date
from typing import Any

import geopandas as gpd
from dhis2_client import DHIS2Client
from dhis2eo import utils
from dhis2eo.data.cds import era5_land
from dhis2eo.integrations.pandas import dataframe_to_dhis2_json
from earthkit import transforms

logger = logging.getLogger(__name__)


def import_era5_land_to_dhis2(
    client: DHIS2Client,
    variable: str,
    data_element_id: str,
    value_col: str,
    value_func: Callable[[Any], Any],
    temporal_aggregation: str,
    spatial_aggregation: str,
    start_date: str,
    end_date: str,
    timezone_offset: int,
    org_unit_level: int,
    dry_run: bool = False,
) -> None:
    """Download ERA5-Land data and import aggregated values into DHIS2."""
    # define the era5 variable names to download
    variables = [variable]

    # parse start and end month
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    start_year, start_month = start.year, start.month
    end_year, end_month = end.year, end.month

    # get org units from DHIS2
    org_units_geojson = client.get_org_units_geojson(level=org_unit_level)
    org_units = gpd.read_file(json.dumps(org_units_geojson))

    # get last imported month, and convert to string to use for comparisons
    # the results contains an `existing` entry which contains information about the last imported period
    # ...for which data was found, or `None` if no existing data was found
    last_imported_response = client.analytics_latest_period_for_level(de_uid=data_element_id, level=org_unit_level)
    logger.debug("Last imported response: %s", last_imported_response)
    last_imported_period = last_imported_response["existing"]
    last_imported_month_string = last_imported_period["id"][:6] if last_imported_period else None

    # loop through and process one month at a time
    for year, month in utils.time.iter_months(start_year, start_month, end_year, end_month):
        month_string = utils.time.dhis2_period(year=year, month=month)
        logger.info("Processing %s", month_string)

        # determine whether data for this month has already been imported
        # we still import if this month is the latest imported one (to allow updates to partially imported months)
        needs_import = last_imported_month_string is None or (month_string >= last_imported_month_string)
        logger.debug("Comparing %s with %s, needs import: %s", month_string, last_imported_month_string, needs_import)

        # only continue if some of the data needs importing
        if not needs_import:
            logger.info("All data already imported for this month")
            continue

        # download era5 data
        logger.info("Downloading data...")
        hourly_data = era5_land.hourly.get(year=year, month=month, variables=variables, bbox=org_units.total_bounds)

        # aggregate to time period
        logger.info("Aggregating time...")
        agg_time = transforms.temporal.daily_reduce(
            hourly_data[value_col],
            how=temporal_aggregation,
            time_shift={"hours": timezone_offset},
            remove_partial_periods=False,
        )

        # aggregate to org units
        logger.info("Aggregating to org units...")
        agg_org_units = transforms.spatial.reduce(
            agg_time,
            org_units,
            mask_dim="id",
            how=spatial_aggregation,
        )
        agg_df = agg_org_units.to_dataframe().reset_index()

        # post-processing
        logger.info("Post-processing...")
        agg_df[value_col] = agg_df[value_col].apply(value_func)

        # create json payload
        logger.info("Creating payload...")
        payload = dataframe_to_dhis2_json(
            df=agg_df,
            org_unit_col="id",
            period_col="valid_time",
            value_col=value_col,
            data_element_id=data_element_id,
        )

        # import to dhis2
        logger.info("Importing...")
        res = client.post("/api/dataValueSets", json=payload, params={"dryRun": str(dry_run).lower()})
        logger.info("Import results: %s", res["response"]["importCount"])
