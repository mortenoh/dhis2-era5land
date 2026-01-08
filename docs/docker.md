# Docker

## Make Targets

```bash
make docker-build   # Build Docker image
make docker-run     # Run import in Docker
make docker-serve   # Start API server in Docker
```

## Building

```bash
docker build -t dhis2-era5land .
```

## Running

### One-time Import

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
DHIS2_BASE_URL=https://your-dhis2-instance.org
DHIS2_USERNAME=your-username
DHIS2_PASSWORD=your-password
DHIS2_START_DATE=2024-01-01
DHIS2_END_DATE=2024-12-31
```

## Docker Compose

The project includes a `compose.yml` file:

```bash
# Run import
docker compose run --rm run

# Start API server
docker compose up serve
```

The compose file automatically uses `.env` if present.

## Pre-built Image

```bash
docker pull ghcr.io/mortenoh/dhis2-era5land:main
docker run --env-file .env ghcr.io/mortenoh/dhis2-era5land:main run
```

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
  --from-literal=DHIS2_BASE_URL=https://your-dhis2.org \
  --from-literal=DHIS2_USERNAME=admin \
  --from-literal=DHIS2_PASSWORD=secret
```
