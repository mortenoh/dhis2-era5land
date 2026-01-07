"""Import ERA5-Land climate data into DHIS2."""

import json
from datetime import date

import geopandas as gpd
from dhis2_client import DHIS2Client
from dhis2eo import utils
from dhis2eo.data.cds import era5_land
from dhis2eo.integrations.pandas import dataframe_to_dhis2_json
from earthkit import transforms

################
# Script Inputs:

# connect to DHIS2
client = DHIS2Client(
    base_url="https://play.im.dhis2.org/stable-2-42-3-1",
    username="admin",
    password="district",
)

# define the ERA5 variable to import
variable = "total_precipitation"  # choose a variable you want to download and go to the "API request"

# define which DHIS2 data element to import data into
data_element_id = "bMoGyfJoH9c"  # update this to the correct DHIS2 data element

# define how to get and process the values
value_col = "tp"  # name of the column that contains the values


def value_processing(value):
    """Convert precipitation from meters to millimeters."""
    return value * 1000


# define how to aggregate the values
temporal_aggregation = (
    "sum"  # this is for total precipitation, but other variables like temperature should be set to 'mean'
)
spatial_aggregation = "mean"  # this should almost always be 'mean'

# define the start and end dates
# for now, this should be gregorian calendar dates only
start_date = "2025-10-01"
end_date = "2025-12-30"

# offset the hourly data from UTC to your local timezone
timezone_offset = 0  # Sierra Leone is UTC+0, so we use an offset of 0

# which level of organisation unit to import data into
org_unit_level = 2


###########################
# Define Reusable Function:


def import_era5_land_to_dhis2(
    client,
    variable,
    data_element_id,
    value_col,
    value_func,
    temporal_aggregation,
    spatial_aggregation,
    start_date,
    end_date,
    timezone_offset,
    org_unit_level,
    dry_run=False,
):
    """Download ERA5-Land data and import aggregated values into DHIS2."""
    # define the era5 variable names to download
    variables = [variable]

    # parse start and end month
    start_date, end_date = date.fromisoformat(start_date), date.fromisoformat(end_date)
    start_year, start_month = start_date.year, start_date.month
    end_year, end_month = end_date.year, end_date.month

    # get org units from DHIS2
    org_units_geojson = client.get_org_units_geojson(level=org_unit_level)
    org_units = gpd.read_file(json.dumps(org_units_geojson))

    # get last imported month, and convert to string to use for comparisons
    # the results contains an `existing` entry which contains information about the last imported period
    # ...for which data was found, or `None` if no existing data was found
    last_imported_response = client.analytics_latest_period_for_level(de_uid=data_element_id, level=org_unit_level)
    print(last_imported_response)
    last_imported_period = last_imported_response["existing"]
    last_imported_month_string = last_imported_period["id"][:6] if last_imported_period else None

    # loop through and process one month at a time
    for year, month in utils.time.iter_months(start_year, start_month, end_year, end_month):
        month_string = utils.time.dhis2_period(year=year, month=month)
        print("")
        print("==================")
        print(f"Processing {month_string}")

        # determine whether data for this month has already been imported
        # we still import if this month is the latest imported one (to allow updates to partially imported months)
        needs_import = last_imported_month_string is None or (month_string >= last_imported_month_string)
        print(f"Comparing {month_string} with {last_imported_month_string}, needs import: {needs_import}")

        # only continue if some of the data needs importing
        if not needs_import:
            print("All data already imported for this month")
            continue

        # download era5 data
        print("Downloading data...")
        hourly_data = era5_land.hourly.get(year=year, month=month, variables=variables, bbox=org_units.total_bounds)

        # aggregate to time period
        print("Aggregating time...")
        agg_time = transforms.temporal.daily_reduce(
            hourly_data[value_col],
            how=temporal_aggregation,
            time_shift={"hours": timezone_offset},
            remove_partial_periods=False,
        )

        # aggregate to org units
        print("Aggregating to org units...")
        agg_org_units = transforms.spatial.reduce(
            agg_time,
            org_units,
            mask_dim="id",
            how=spatial_aggregation,
        )
        agg_df = agg_org_units.to_dataframe().reset_index()

        # post-processing
        print("Post-processing...")
        agg_df[value_col] = agg_df[value_col].apply(value_func)

        # create json payload
        print("Creating payload...")
        payload = dataframe_to_dhis2_json(
            df=agg_df,
            org_unit_col="id",
            period_col="valid_time",
            value_col=value_col,
            data_element_id=data_element_id,
        )

        # import to dhis2
        print("Importing...")
        res = client.post("/api/dataValueSets", json=payload, params={"dryRun": str(dry_run).lower()})
        print(f"--> Import results: {res['response']['importCount']}")


##########################
# Run the import function:

if __name__ == "__main__":
    import_era5_land_to_dhis2(
        client,
        variable=variable,
        data_element_id=data_element_id,
        value_col=value_col,
        value_func=value_processing,
        temporal_aggregation=temporal_aggregation,
        spatial_aggregation=spatial_aggregation,
        start_date=start_date,
        end_date=end_date,
        timezone_offset=timezone_offset,
        org_unit_level=org_unit_level,
    )
