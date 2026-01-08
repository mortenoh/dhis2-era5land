"""Pydantic models for API responses."""

from pydantic import BaseModel

from dhis2_era5land import __version__


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str = __version__


class ImportResponse(BaseModel):
    """Import response."""

    status: str
    message: str
