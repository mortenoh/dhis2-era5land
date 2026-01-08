# Configuration

All settings can be configured via environment variables or a `.env` file. CLI options override environment settings.

## CDS API

The [Climate Data Store API](https://cds.climate.copernicus.eu/how-to-api) is required to download ERA5-Land data.

| Environment Variable | Default |
|---------------------|---------|
| `CDSAPI_URL` | `https://cds.climate.copernicus.eu/api` |
| `CDSAPI_KEY` | **required** ([get one here](https://cds.climate.copernicus.eu/how-to-api)) |

## DHIS2 Settings

| Environment Variable | Default |
|---------------------|---------|
| `DHIS2_BASE_URL` | **required** |
| `DHIS2_USERNAME` | **required** |
| `DHIS2_PASSWORD` | **required** |
| `DHIS2_DATA_ELEMENT_ID` | **required** |
| `DHIS2_START_DATE` | `2025-01-01` |
| `DHIS2_END_DATE` | `2025-01-07` |
| `DHIS2_VARIABLE` | `total_precipitation` |
| `DHIS2_VALUE_COL` | `tp` |
| `DHIS2_VALUE_TRANSFORM` | `meters_to_millimeters` |
| `DHIS2_TEMPORAL_AGGREGATION` | `sum` |
| `DHIS2_SPATIAL_AGGREGATION` | `mean` |
| `DHIS2_TIMEZONE_OFFSET` | `0` |
| `DHIS2_ORG_UNIT_LEVEL` | `2` |

## Scheduler Settings

| Environment Variable | Default |
|---------------------|---------|
| `DHIS2_CRON` | `0 1 * * *` (daily at 1am) |

See [Scheduling](scheduling.md) for cron expression examples.

## Example `.env` File

```env
# CDS API (required - get key from https://cds.climate.copernicus.eu/how-to-api)
CDSAPI_KEY=your-cds-api-key

# DHIS2 connection (required)
DHIS2_BASE_URL=https://your-dhis2-instance.org
DHIS2_USERNAME=your-username
DHIS2_PASSWORD=your-password
DHIS2_DATA_ELEMENT_ID=your-data-element-id

# Date range to import
DHIS2_START_DATE=2024-01-01
DHIS2_END_DATE=2024-12-31

# Schedule (optional - for scheduler mode)
DHIS2_CRON=0 6 * * *
```

## Priority

Configuration is loaded in this order (later overrides earlier):

1. Default values (lowest priority)
2. Environment variables
3. `.env` file
4. CLI arguments (highest priority)

## API Server Options

When running `dhis2-era5land serve`:

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | Host to bind to | `0.0.0.0` |
| `--port` | Port to listen on | `8080` |
| `-v, --verbose` | Enable debug logging | `false` |

## Security Note

`DHIS2_PASSWORD` can only be set via `.env` or environment variable (not CLI) for security reasons.
