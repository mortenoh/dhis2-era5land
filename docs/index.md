# dhis2-era5land

Import ERA5-Land climate data into DHIS2.

## Overview

This tool downloads ERA5-Land climate data from the Copernicus Climate Data Store, aggregates it temporally and spatially to match DHIS2 organisation units, and imports the values into DHIS2.

## Features

- Download ERA5-Land hourly data for any variable
- Temporal aggregation (sum, mean) to daily/monthly periods
- Spatial aggregation to DHIS2 organisation unit boundaries
- Configurable value transforms (unit conversion)
- Incremental import (skips already imported periods)
- Dry run mode for testing

## Quick Start

```bash
# Install
uv tool install dhis2-era5land --from git+https://github.com/mortenoh/dhis2-era5land

# Run
dhis2-era5land --start-date 2024-01-01 --end-date 2024-03-31
```

## Requirements

- Python 3.12+
- Access to a DHIS2 instance
- ERA5-Land data access via dhis2eo library
