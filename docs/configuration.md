# Configuration

All settings can be configured via environment variables (prefix `DHIS2_`) or a `.env` file. CLI options override environment settings.

## Environment Variables

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

## Example `.env` File

```env
DHIS2_BASE_URL=https://your-dhis2-instance.org
DHIS2_USERNAME=your-username
DHIS2_PASSWORD=your-password
DHIS2_START_DATE=2024-01-01
DHIS2_END_DATE=2024-12-31
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
