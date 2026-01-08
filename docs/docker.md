# Docker

## Scheduled Imports (Recommended)

The easiest way to run automated imports:

```bash
# 1. Create .env file with your credentials
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

# 2. Start the scheduler (runs daily at 6am)
docker compose -f compose.ghcr.yml up -d schedule

# 3. View logs
docker compose -f compose.ghcr.yml logs -f schedule
```

Get your CDS API key from: https://cds.climate.copernicus.eu/how-to-api

See [Scheduling](scheduling.md) for more options and cron examples.

## One-time Import

```bash
docker run --env-file .env dhis2-era5land run
```

With options:
```bash
docker run --env-file .env dhis2-era5land run \
  --start-date 2024-01-01 \
  --end-date 2024-03-31 \
  --dry-run
```

### API Server

```bash
docker run -p 8080:8080 --env-file .env dhis2-era5land serve
```

## Environment File

Create a `.env` file:

```env
# CDS API (required)
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

## Docker Compose

### Pre-built Image (recommended)

Use `compose.ghcr.yml` with the pre-built multi-arch image from GHCR:

```bash
# Start scheduler (recommended for production)
docker compose -f compose.ghcr.yml up -d schedule

# Run one-time import
docker compose -f compose.ghcr.yml run --rm run

# Start API server
docker compose -f compose.ghcr.yml up serve
```

### Build Locally

Use `compose.yml` to build the image locally:

```bash
# Start scheduler
docker compose up -d schedule

# Run one-time import
docker compose run --rm run

# Start API server
docker compose up serve
```

Both compose files automatically use `.env` if present.

## Kubernetes CronJob

Example for scheduled imports:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dhis2-era5land-import
spec:
  schedule: "0 6 1 * *"  # Monthly on the 1st at 6am
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: importer
            image: dhis2-era5land:latest
            args: ["run"]
            envFrom:
            - secretRef:
                name: dhis2-credentials
          restartPolicy: OnFailure
```

Create the secret:

```bash
kubectl create secret generic dhis2-credentials \
  --from-literal=CDSAPI_KEY=your-cds-api-key \
  --from-literal=DHIS2_BASE_URL=https://your-dhis2.org \
  --from-literal=DHIS2_USERNAME=admin \
  --from-literal=DHIS2_PASSWORD=secret \
  --from-literal=DHIS2_DATA_ELEMENT_ID=your-data-element-id
```
