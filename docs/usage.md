# Usage

## Installation

```bash
# Install as a global tool
uv tool install dhis2-era5land --from git+https://github.com/mortenoh/dhis2-era5land

# Or run directly without installing
uvx --from git+https://github.com/mortenoh/dhis2-era5land dhis2-era5land --help
```

## Basic Usage

```bash
# Run with custom date range
dhis2-era5land --start-date 2024-01-01 --end-date 2024-03-31

# Dry run (no actual import)
dhis2-era5land --dry-run -v

# Import temperature data
dhis2-era5land --variable 2m_temperature --value-transform kelvin_to_celsius
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
| `--value-transform` | Value transform | `meters_to_millimeters` |
| `--temporal-aggregation` | Temporal aggregation (`sum`, `mean`) | `sum` |
| `--spatial-aggregation` | Spatial aggregation | `mean` |
| `--timezone-offset` | Timezone offset in hours | `0` |
| `--org-unit-level` | Org unit level | `2` |
| `--dry-run` | Don't actually import | `false` |
| `-v, --verbose` | Enable debug logging | `false` |

## Value Transforms

| Transform | Description |
|-----------|-------------|
| `meters_to_millimeters` | Precipitation (m to mm) |
| `meters_to_centimeters` | Snow depth (m to cm) |
| `kelvin_to_celsius` | Temperature (K to C) |
| `kelvin_to_fahrenheit` | Temperature (K to F) |
| `identity` | No transformation |
