# Usage

## Installation

```bash
# Install as a global tool
uv tool install dhis2-era5land --from git+https://github.com/mortenoh/dhis2-era5land

# Or run directly without installing
uvx --from git+https://github.com/mortenoh/dhis2-era5land dhis2-era5land --help
```

## CLI Commands

### run

Run a one-time import:

```bash
# Basic usage
dhis2-era5land run --start-date 2024-01-01 --end-date 2024-03-31

# Dry run with verbose logging
dhis2-era5land run --dry-run -v

# Import temperature data
dhis2-era5land run --variable 2m_temperature --value-transform kelvin_to_celsius
```

### serve

Start the API server:

```bash
# Default (port 8080)
dhis2-era5land serve

# Custom port with verbose logging
dhis2-era5land serve --port 3000 -v
```

## CLI Options (run)

| Option | Description | Default |
|--------|-------------|---------|
| `--start-date` | Start date (YYYY-MM-DD) | `2025-10-01` |
| `--end-date` | End date (YYYY-MM-DD) | `2025-12-30` |
| `--base-url` | DHIS2 base URL | `https://play.im.dhis2.org/stable-2-42-3-1` |
| `--username` | DHIS2 username | `admin` |
| `--variable` | ERA5 variable name | `total_precipitation` |
| `--data-element-id` | DHIS2 data element ID | `bMoGyfJoH9c` |
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

### GET /health

Health check endpoint.

```bash
curl http://localhost:8080/health
```

Response:
```json
{"status": "ok", "version": "0.1.0"}
```

### GET /status

Get current import status.

```bash
curl http://localhost:8080/status
```

Response:
```json
{
  "status": "idle",
  "started_at": null,
  "completed_at": null,
  "error": null,
  "last_result": null
}
```

Status values: `idle`, `running`, `completed`, `failed`

### POST /import

Trigger an import job.

```bash
curl -X POST http://localhost:8080/import \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2024-01-01", "end_date": "2024-03-31", "dry_run": true}'
```

Request body (all fields optional, defaults from settings):
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-03-31",
  "variable": "total_precipitation",
  "data_element_id": "bMoGyfJoH9c",
  "value_col": "tp",
  "value_transform": "meters_to_millimeters",
  "temporal_aggregation": "sum",
  "spatial_aggregation": "mean",
  "timezone_offset": 0,
  "org_unit_level": 2,
  "dry_run": false
}
```

## Value Transforms

| Transform | Description |
|-----------|-------------|
| `meters_to_millimeters` | Precipitation (m to mm) |
| `meters_to_centimeters` | Snow depth (m to cm) |
| `kelvin_to_celsius` | Temperature (K to C) |
| `kelvin_to_fahrenheit` | Temperature (K to F) |
| `identity` | No transformation |
