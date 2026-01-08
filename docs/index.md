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
- **Scheduled imports** with cron-based Docker scheduler
- **CLI mode** for one-time imports
- **API mode** for HTTP-triggered imports

## Quick Start (Scheduled Imports)

The easiest way to run automated imports:

```bash
# 1. Create .env file
cat > .env << 'EOF'
CDSAPI_KEY=your-cds-api-key
DHIS2_BASE_URL=https://your-dhis2-instance.org
DHIS2_USERNAME=your-username
DHIS2_PASSWORD=your-password
DHIS2_DATA_ELEMENT_ID=your-data-element-id
DHIS2_START_DATE=2024-01-01
DHIS2_END_DATE=2024-12-31
DHIS2_CRON=0 6 * * *
EOF

# 2. Start scheduler (runs daily at 6am)
docker compose -f compose.ghcr.yml up -d schedule

# 3. View logs
docker compose -f compose.ghcr.yml logs -f schedule
```

Get your CDS API key from: https://cds.climate.copernicus.eu/how-to-api

See [Scheduling](scheduling.md) for more options.

## One-time Import

```bash
# Using Docker (recommended)
docker compose -f compose.ghcr.yml run --rm run

# Or install locally
uv tool install dhis2-era5land --from git+https://github.com/mortenoh/dhis2-era5land
dhis2-era5land run --start-date 2024-01-01 --end-date 2024-03-31
```

## Requirements

- [CDS API key](https://cds.climate.copernicus.eu/how-to-api) for ERA5-Land data access
- Access to a DHIS2 instance
- Docker (recommended) or Python 3.12+
