# dhis2-era5land

[![CI](https://github.com/mortenoh/dhis2-era5land/actions/workflows/ci.yml/badge.svg)](https://github.com/mortenoh/dhis2-era5land/actions/workflows/ci.yml)
[![Docker](https://github.com/mortenoh/dhis2-era5land/actions/workflows/docker.yml/badge.svg)](https://github.com/mortenoh/dhis2-era5land/actions/workflows/docker.yml)
[![Docs](https://github.com/mortenoh/dhis2-era5land/actions/workflows/docs.yml/badge.svg)](https://mortenoh.github.io/dhis2-era5land/)
[![GHCR](https://img.shields.io/badge/ghcr.io-mortenoh%2Fdhis2--era5land-blue)](https://github.com/mortenoh/dhis2-era5land/pkgs/container/dhis2-era5land)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Import ERA5-Land climate data into DHIS2.

## Installation

```bash
# Install as a global tool
uv tool install dhis2-era5land --from git+https://github.com/mortenoh/dhis2-era5land

# Or run directly without installing
uvx --from git+https://github.com/mortenoh/dhis2-era5land dhis2-era5land --help
```

## Commands

### run

Run a one-time import:

```bash
dhis2-era5land run --start-date 2024-01-01 --end-date 2024-03-31
dhis2-era5land run --dry-run -v
dhis2-era5land run --variable 2m_temperature --value-transform kelvin_to_celsius
```

### serve

Start the API server:

```bash
dhis2-era5land serve
dhis2-era5land serve --port 3000 -v
```

## CLI Options (run)

| Option | Description | Default |
|--------|-------------|---------|
| `--start-date` | Start date (YYYY-MM-DD) | `2025-01-01` |
| `--end-date` | End date (YYYY-MM-DD) | `2025-01-07` |
| `--base-url` | DHIS2 base URL | **required** |
| `--username` | DHIS2 username | **required** |
| `--variable` | ERA5 variable name | `total_precipitation` |
| `--data-element-id` | DHIS2 data element ID | **required** |
| `--value-col` | Value column name | `tp` |
| `--value-transform` | Value transform | `meters_to_millimeters` |
| `--temporal-aggregation` | Temporal aggregation (`sum`, `mean`) | `sum` |
| `--spatial-aggregation` | Spatial aggregation | `mean` |
| `--timezone-offset` | Timezone offset in hours | `0` |
| `--org-unit-level` | Org unit level | `2` |
| `--dry-run` | Don't actually import | `false` |
| `-v, --verbose` | Enable debug logging | `false` |

## CLI Options (serve)

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | Host to bind to | `0.0.0.0` |
| `--port` | Port to listen on | `8080` |
| `-v, --verbose` | Enable debug logging | `false` |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/$import` | POST | Run an import (blocks until complete) |

### POST /$import

All configuration from environment variables. Only `dryRun` query param supported.

```bash
# Run import
curl -X POST http://localhost:8080/\$import

# Dry run
curl -X POST "http://localhost:8080/\$import?dryRun=true"
```

## Value Transforms

| Transform | Description |
|-----------|-------------|
| `meters_to_millimeters` | Precipitation (m to mm) |
| `meters_to_centimeters` | Snow depth (m to cm) |
| `kelvin_to_celsius` | Temperature (K to C) |
| `kelvin_to_fahrenheit` | Temperature (K to F) |
| `identity` | No transformation |

## Configuration

Environment variables or `.env` file. CLI options override environment settings.

| Environment Variable | Default |
|---------------------|---------|
| `CDSAPI_URL` | `https://cds.climate.copernicus.eu/api` |
| `CDSAPI_KEY` | - |
| `DHIS2_BASE_URL` | **required** |
| `DHIS2_USERNAME` | **required** |
| `DHIS2_PASSWORD` | **required** |
| `DHIS2_VARIABLE` | `total_precipitation` |
| `DHIS2_DATA_ELEMENT_ID` | **required** |
| `DHIS2_VALUE_COL` | `tp` |
| `DHIS2_VALUE_TRANSFORM` | `meters_to_millimeters` |
| `DHIS2_TEMPORAL_AGGREGATION` | `sum` |
| `DHIS2_SPATIAL_AGGREGATION` | `mean` |
| `DHIS2_START_DATE` | `2025-01-01` |
| `DHIS2_END_DATE` | `2025-01-07` |
| `DHIS2_TIMEZONE_OFFSET` | `0` |
| `DHIS2_ORG_UNIT_LEVEL` | `2` |
| `DHIS2_CRON` | - (scheduler only) |

Example `.env` file:

```env
# CDS API (get key from https://cds.climate.copernicus.eu/how-to-api)
CDSAPI_URL=https://cds.climate.copernicus.eu/api
CDSAPI_KEY=your-cds-api-key

# DHIS2 connection
DHIS2_BASE_URL=https://your-dhis2-instance.org
DHIS2_USERNAME=your-username
DHIS2_PASSWORD=your-password
DHIS2_DATA_ELEMENT_ID=your-data-element-id
DHIS2_START_DATE=2024-01-01
DHIS2_END_DATE=2024-12-31
```

Note: `DHIS2_PASSWORD` can only be set via `.env` or environment variable (not CLI) for security.

## Docker

### Pre-built Image (recommended)

Using the pre-built image from GHCR:

```bash
# Run import
docker compose -f compose.ghcr.yml run --rm run

# Start API server
docker compose -f compose.ghcr.yml up serve
```

### Build Locally

```bash
# Run import (builds locally)
docker compose run --rm run

# Start API server (builds locally)
docker compose up serve
```

### Scheduled Imports

Run automated imports on a cron schedule:

```bash
# Add to .env
DHIS2_CRON=0 6 * * *  # Daily at 6am

# Start scheduler
docker compose -f compose.ghcr.yml up schedule
```

See [scheduling documentation](https://mortenoh.github.io/dhis2-era5land/scheduling/) for details.

### Manual

```bash
# Build
docker build -t dhis2-era5land .

# Run import
docker run --env-file .env dhis2-era5land run

# Start API server
docker run -p 8080:8080 --env-file .env dhis2-era5land serve
```

## Development

Requires Python 3.12+.

```bash
make install   # Install dependencies
make lint      # Run ruff, mypy, pyright (with auto-fix)
make test      # Run tests
make docs      # Build documentation
make clean     # Clean up cache files
```
