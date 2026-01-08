"""FastAPI server for ERA5-Land to DHIS2 import."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dhis2_client import DHIS2Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from dhis2_era5land.importer import import_era5_land_to_dhis2
from dhis2_era5land.settings import settings
from dhis2_era5land.transforms import Transform, get_transform

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


class ImportRequest(BaseModel):
    """Import request parameters."""

    start_date: str | None = None
    end_date: str | None = None
    variable: str | None = None
    data_element_id: str  # Required
    value_col: str | None = None
    value_transform: str | None = None
    temporal_aggregation: str | None = None
    spatial_aggregation: str | None = None
    timezone_offset: int | None = None
    org_unit_level: int | None = None
    dry_run: bool = False


class ImportResponse(BaseModel):
    """Import response."""

    status: str
    message: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.post("/import", response_model=ImportResponse)
def run_import(request: ImportRequest) -> ImportResponse:
    """Run an import (blocks until complete)."""
    try:
        # Use request values or fall back to settings
        start_date = request.start_date or settings.start_date
        end_date = request.end_date or settings.end_date
        variable = request.variable or settings.variable
        value_col = request.value_col or settings.value_col
        value_transform = request.value_transform or settings.value_transform
        temporal_aggregation = request.temporal_aggregation or settings.temporal_aggregation
        spatial_aggregation = request.spatial_aggregation or settings.spatial_aggregation
        timezone_offset = request.timezone_offset if request.timezone_offset is not None else settings.timezone_offset
        org_unit_level = request.org_unit_level if request.org_unit_level is not None else settings.org_unit_level

        # Create DHIS2 client (settings validated at startup)
        client = DHIS2Client(
            base_url=settings.base_url,
            username=settings.username,
            password=settings.password,
        )

        # Get transform function
        transform = Transform(value_transform) if isinstance(value_transform, str) else value_transform
        value_func = get_transform(transform)

        # Run import
        import_era5_land_to_dhis2(
            client=client,
            variable=variable,
            data_element_id=request.data_element_id,
            value_col=value_col,
            value_func=value_func,
            temporal_aggregation=temporal_aggregation,
            spatial_aggregation=spatial_aggregation,
            start_date=start_date,
            end_date=end_date,
            timezone_offset=timezone_offset,
            org_unit_level=org_unit_level,
            dry_run=request.dry_run,
        )

        return ImportResponse(status="ok", message="Import completed successfully")

    except Exception as e:
        logger.exception("Import failed")
        raise HTTPException(status_code=500, detail=str(e)) from e
