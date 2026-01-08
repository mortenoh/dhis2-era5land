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
- **CLI mode** for one-time or scheduled imports
- **API mode** for HTTP-triggered imports

## Quick Start

```bash
# Install
uv tool install dhis2-era5land --from git+https://github.com/mortenoh/dhis2-era5land

# Run import
dhis2-era5land run --start-date 2024-01-01 --end-date 2024-03-31

# Or start API server
dhis2-era5land serve
```

## Docker

```bash
# Build
docker build -t dhis2-era5land .

# Run import
docker run --env-file .env dhis2-era5land run

# Start API server
docker run -p 8080:8080 --env-file .env dhis2-era5land serve
```

## Requirements

- Python 3.12+
- [CDS API key](https://cds.climate.copernicus.eu/how-to-api) for ERA5-Land data access
- Access to a DHIS2 instance
