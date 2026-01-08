"""FastAPI server for ERA5-Land to DHIS2 import."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dhis2_client import DHIS2Client
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from dhis2_era5land.importer import import_era5_land_to_dhis2
from dhis2_era5land.settings import settings
from dhis2_era5land.transforms import get_transform

logger = logging.getLogger(__name__)


def validate_settings() -> None:
    """Validate required settings at startup."""
    missing: list[str] = []
    if not settings.base_url:
        missing.append("DHIS2_BASE_URL")
    if not settings.username:
        missing.append("DHIS2_USERNAME")
    if not settings.password:
        missing.append("DHIS2_PASSWORD")
    if not settings.data_element_id:
        missing.append("DHIS2_DATA_ELEMENT_ID")
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Validate settings on startup."""
    validate_settings()
    logger.info("Settings validated, server starting")
    yield


app = FastAPI(
    title="dhis2-era5land",
    description="Import ERA5-Land climate data into DHIS2",
    lifespan=lifespan,
)


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str = "0.1.0"


class ImportResponse(BaseModel):
    """Import response."""

    status: str
    message: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.post("/$import", response_model=ImportResponse)
def run_import(dryRun: bool = Query(default=False)) -> ImportResponse:
    """Run an import (blocks until complete). All config from environment."""
    try:
        client = DHIS2Client(
            base_url=settings.base_url,  # type: ignore[arg-type]
            username=settings.username,  # type: ignore[arg-type]
            password=settings.password,  # type: ignore[arg-type]
        )

        value_func = get_transform(settings.value_transform)

        import_era5_land_to_dhis2(
            client=client,
            variable=settings.variable,
            data_element_id=settings.data_element_id,  # type: ignore[arg-type]
            value_col=settings.value_col,
            value_func=value_func,
            temporal_aggregation=settings.temporal_aggregation,
            spatial_aggregation=settings.spatial_aggregation,
            start_date=settings.start_date,
            end_date=settings.end_date,
            timezone_offset=settings.timezone_offset,
            org_unit_level=settings.org_unit_level,
            dry_run=dryRun,
        )

        return ImportResponse(status="ok", message="Import completed successfully")

    except Exception as e:
        logger.exception("Import failed")
        raise HTTPException(status_code=500, detail=str(e)) from e
