# Scheduling

Run automated imports on a schedule using the built-in scheduler.

## Quick Start

```bash
# Set cron schedule in .env
echo "DHIS2_CRON=0 6 * * *" >> .env

# Start scheduler
docker compose up schedule
```

## How It Works

The scheduler mode uses system cron inside the container:

1. Container starts and reads `DHIS2_CRON` environment variable
2. Creates a crontab entry with the specified schedule
3. Runs `cron` daemon in foreground
4. On each trigger, spawns `dhis2-era5land run` as a separate process

This provides **process isolation** - if an import fails or crashes, it doesn't affect the scheduler.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CDSAPI_URL` | No | CDS API URL (default: `https://cds.climate.copernicus.eu/api`) |
| `CDSAPI_KEY` | No | CDS API key ([get one here](https://cds.climate.copernicus.eu/how-to-api)) |
| `DHIS2_CRON` | No | Cron expression (default: `0 1 * * *`) |
| `DHIS2_START_DATE` | Yes | Start date for imports |
| `DHIS2_END_DATE` | Yes | End date for imports |
| `DHIS2_BASE_URL` | Yes | DHIS2 instance URL |
| `DHIS2_USERNAME` | Yes | DHIS2 username |
| `DHIS2_PASSWORD` | Yes | DHIS2 password |
| `DHIS2_DATA_ELEMENT_ID` | Yes | Target data element |

## Cron Expression Examples

| Expression | Description |
|------------|-------------|
| `0 6 * * *` | Daily at 6:00 AM |
| `0 0 * * *` | Daily at midnight |
| `0 6 * * 1` | Weekly on Monday at 6:00 AM |
| `0 0 1 * *` | Monthly on the 1st at midnight |
| `*/5 * * * *` | Every 5 minutes (for testing) |

## Docker Compose

### Using Pre-built Image (recommended)

```bash
docker compose -f compose.ghcr.yml up schedule
```

### Building Locally

```bash
docker compose up schedule
```

## Example .env File

```env
# CDS API (required)
CDSAPI_URL=https://cds.climate.copernicus.eu/api
CDSAPI_KEY=your-cds-api-key

# Schedule (optional, defaults to daily at 1am)
DHIS2_CRON=0 6 * * *

# Date range
DHIS2_START_DATE=2024-01-01
DHIS2_END_DATE=2024-12-31

# DHIS2 connection
DHIS2_BASE_URL=https://your-dhis2-instance.org
DHIS2_USERNAME=your-username
DHIS2_PASSWORD=your-password
DHIS2_DATA_ELEMENT_ID=your-data-element-id

# ERA5 config (optional, has defaults)
DHIS2_VARIABLE=total_precipitation
DHIS2_VALUE_TRANSFORM=meters_to_millimeters
```

## Viewing Logs

```bash
# Follow logs
docker compose logs -f schedule

# View last 100 lines
docker compose logs --tail 100 schedule
```

## Manual Trigger

To manually trigger an import while scheduler is running:

```bash
docker compose exec schedule dhis2-era5land run
```

## Kubernetes

For Kubernetes deployments, consider using a CronJob instead of the built-in scheduler. See [Docker documentation](docker.md#kubernetes-cronjob) for an example.
