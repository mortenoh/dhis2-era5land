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

Note: `DHIS2_PASSWORD` must be set via environment variable (not CLI) for security.

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

### POST /$import

Run an import (blocks until complete). All configuration from environment variables.

```bash
# Run import
curl -X POST http://localhost:8080/\$import

# Dry run
curl -X POST "http://localhost:8080/\$import?dryRun=true"
```

Response:
```json
{"status": "ok", "message": "Import completed successfully"}
```

## Value Transforms

| Transform | Description |
|-----------|-------------|
| `meters_to_millimeters` | Precipitation (m to mm) |
| `meters_to_centimeters` | Snow depth (m to cm) |
| `kelvin_to_celsius` | Temperature (K to C) |
| `kelvin_to_fahrenheit` | Temperature (K to F) |
| `identity` | No transformation |
