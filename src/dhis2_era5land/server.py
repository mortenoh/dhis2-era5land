"""FastAPI server for ERA5-Land to DHIS2 import."""

import logging
import threading
from datetime import datetime
from enum import StrEnum
from typing import Any

from dhis2_client import DHIS2Client
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

from dhis2_era5land.importer import import_era5_land_to_dhis2
from dhis2_era5land.settings import settings
from dhis2_era5land.transforms import Transform, get_transform

logger = logging.getLogger(__name__)


class ImportStatus(StrEnum):
    """Import job status."""

    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ImportState(BaseModel):
    """Current import state."""

    status: ImportStatus = ImportStatus.IDLE
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None
    last_result: dict[str, Any] | None = None


# Global state for tracking import status
_state = ImportState()
_lock = threading.Lock()


app = FastAPI(
    title="dhis2-era5land",
    description="Import ERA5-Land climate data into DHIS2",
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
    data_element_id: str | None = None
    value_col: str | None = None
    value_transform: str | None = None
    temporal_aggregation: str | None = None
    spatial_aggregation: str | None = None
    timezone_offset: int | None = None
    org_unit_level: int | None = None
    dry_run: bool = False


class ImportResponse(BaseModel):
    """Import response."""

    message: str
    status: ImportStatus


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.get("/status", response_model=ImportState)
def status() -> ImportState:
    """Get current import status."""
    with _lock:
        return _state.model_copy()


@app.post("/import", response_model=ImportResponse)
def trigger_import(
    request: ImportRequest,
    background_tasks: BackgroundTasks,
) -> ImportResponse:
    """Trigger an import job."""
    with _lock:
        if _state.status == ImportStatus.RUNNING:
            return ImportResponse(
                message="Import already running",
                status=_state.status,
            )

    background_tasks.add_task(run_import, request)
    return ImportResponse(
        message="Import started",
        status=ImportStatus.RUNNING,
    )


def run_import(request: ImportRequest) -> None:
    """Run the import job in the background."""
    global _state

    with _lock:
        _state = ImportState(
            status=ImportStatus.RUNNING,
            started_at=datetime.now(),
        )

    try:
        # Use request values or fall back to settings
        start_date = request.start_date or settings.start_date
        end_date = request.end_date or settings.end_date
        variable = request.variable or settings.variable
        data_element_id = request.data_element_id or settings.data_element_id
        value_col = request.value_col or settings.value_col
        value_transform = request.value_transform or settings.value_transform
        temporal_aggregation = request.temporal_aggregation or settings.temporal_aggregation
        spatial_aggregation = request.spatial_aggregation or settings.spatial_aggregation
        timezone_offset = request.timezone_offset if request.timezone_offset is not None else settings.timezone_offset
        org_unit_level = request.org_unit_level if request.org_unit_level is not None else settings.org_unit_level

        # Create DHIS2 client
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
            data_element_id=data_element_id,
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

        with _lock:
            _state = ImportState(
                status=ImportStatus.COMPLETED,
                started_at=_state.started_at,
                completed_at=datetime.now(),
                last_result={"message": "Import completed successfully"},
            )
        logger.info("Import completed successfully")

    except Exception as e:
        logger.exception("Import failed")
        with _lock:
            _state = ImportState(
                status=ImportStatus.FAILED,
                started_at=_state.started_at,
                completed_at=datetime.now(),
                error=str(e),
            )
