# dhis2-era5land

Import ERA5-Land climate data into DHIS2.

## Installation

```bash
# Install as a global tool
uv tool install dhis2-era5land --from git+https://github.com/mortenoh/dhis2-era5land

# Or run directly without installing
uvx --from git+https://github.com/mortenoh/dhis2-era5land dhis2-era5land --help
```

## Usage

```bash
dhis2-era5land --start-date 2024-01-01 --end-date 2024-03-31
dhis2-era5land --dry-run -v
dhis2-era5land --variable 2m_temperature --value-transform kelvin_to_celsius
```

## Options

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

### Value Transforms

| Transform | Description |
|-----------|-------------|
| `meters_to_millimeters` | Precipitation (m to mm) |
| `meters_to_centimeters` | Snow depth (m to cm) |
| `kelvin_to_celsius` | Temperature (K to C) |
| `kelvin_to_fahrenheit` | Temperature (K to F) |
| `identity` | No transformation |

## Configuration

Environment variables (prefix `DHIS2_`) or `.env` file. CLI options override environment settings.

| Environment Variable | Default |
|---------------------|---------|
| `DHIS2_BASE_URL` | `https://play.im.dhis2.org/stable-2-42-3-1` |
| `DHIS2_USERNAME` | `admin` |
| `DHIS2_PASSWORD` | `district` |
| `DHIS2_VARIABLE` | `total_precipitation` |
| `DHIS2_DATA_ELEMENT_ID` | `bMoGyfJoH9c` |
| `DHIS2_VALUE_COL` | `tp` |
| `DHIS2_VALUE_TRANSFORM` | `meters_to_millimeters` |
| `DHIS2_TEMPORAL_AGGREGATION` | `sum` |
| `DHIS2_SPATIAL_AGGREGATION` | `mean` |
| `DHIS2_START_DATE` | `2025-10-01` |
| `DHIS2_END_DATE` | `2025-12-30` |
| `DHIS2_TIMEZONE_OFFSET` | `0` |
| `DHIS2_ORG_UNIT_LEVEL` | `2` |

Example `.env` file:

```env
DHIS2_BASE_URL=https://your-dhis2-instance.org
DHIS2_USERNAME=your-username
DHIS2_PASSWORD=your-password
DHIS2_START_DATE=2024-01-01
DHIS2_END_DATE=2024-12-31
```

Note: `DHIS2_PASSWORD` can only be set via `.env` or environment variable (not CLI) for security.

## Development

Requires Python 3.12+.

```bash
make install   # Install dependencies
make lint      # Run ruff, mypy, pyright (with auto-fix)
make test      # Run tests
make run       # Run the import
make clean     # Clean up cache files
```
