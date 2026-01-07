"""Configuration for ERA5-Land to DHIS2 import."""

from dhis2_client import DHIS2Client

from dhis2_era5land.transforms import meters_to_millimeters

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
value_processing = meters_to_millimeters  # transform function for values

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
