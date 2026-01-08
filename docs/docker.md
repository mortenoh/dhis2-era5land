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

### Pre-built Image (recommended)

Use `compose.ghcr.yml` with the pre-built multi-arch image from GHCR:

```bash
# Run import
docker compose -f compose.ghcr.yml run --rm run

# Start API server
docker compose -f compose.ghcr.yml up serve
```

### Build Locally

Use `compose.yml` to build the image locally:

```bash
# Run import
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
  --from-literal=DHIS2_BASE_URL=https://your-dhis2.org \
  --from-literal=DHIS2_USERNAME=admin \
  --from-literal=DHIS2_PASSWORD=secret
```
