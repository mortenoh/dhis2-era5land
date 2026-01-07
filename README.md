# dhis2-era5land

Import ERA5-Land climate data into DHIS2.

## Installation

```bash
uv sync
```

## Usage

```bash
# Run with defaults
uv run dhis2-era5land

# Run with custom date range
uv run dhis2-era5land --start-date 2024-01-01 --end-date 2024-03-31

# Dry run (no actual import)
uv run dhis2-era5land --dry-run

# Verbose logging
uv run dhis2-era5land -v
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--start-date` | Start date (YYYY-MM-DD) | `2025-10-01` |
| `--end-date` | End date (YYYY-MM-DD) | `2025-12-30` |
| `--base-url` | DHIS2 base URL | `https://play.im.dhis2.org/stable-2-42-3-1` |
| `--username` | DHIS2 username | `admin` |
| `--variable` | ERA5 variable name | `total_precipitation` |
| `--data-element-id` | DHIS2 data element ID | `bMoGyfJoH9c` |
| `--value-col` | Value column name | `tp` |
| `--value-transform` | Value transform (`meters_to_millimeters`, `meters_to_centimeters`, `kelvin_to_celsius`, `kelvin_to_fahrenheit`, `identity`) | `meters_to_millimeters` |
| `--temporal-aggregation` | Temporal aggregation (`sum`, `mean`) | `sum` |
| `--spatial-aggregation` | Spatial aggregation | `mean` |
| `--timezone-offset` | Timezone offset in hours | `0` |
| `--org-unit-level` | Org unit level | `2` |
| `--dry-run` | Don't actually import | `false` |
| `--verbose`, `-v` | Enable debug logging | `false` |

## Configuration

### `.env` file

Create a `.env` file in the project root:

```bash
DHIS2_BASE_URL=https://your-dhis2-instance.org
DHIS2_USERNAME=your-username
DHIS2_PASSWORD=your-password
DHIS2_START_DATE=2024-01-01
DHIS2_END_DATE=2024-12-31
```

### Environment variables

All settings can also be set as environment variables with `DHIS2_` prefix.

### Priority

CLI arguments > `.env` file > environment variables > defaults

Note: `DHIS2_PASSWORD` can only be set via `.env` or environment variable (not CLI) for security.
