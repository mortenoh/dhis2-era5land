FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    g++ \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install dependencies
RUN uv sync --frozen --no-dev


FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install runtime dependencies and cron for scheduler mode
RUN apt-get update && apt-get install -y \
    libgeos-c1v5 \
    libproj25 \
    libexpat1 \
    cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /app /app

# Copy entrypoint script
COPY scripts/docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD []
