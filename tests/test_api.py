"""Tests for API server."""

from fastapi.testclient import TestClient

from dhis2_era5land.server import ImportStatus, app

client = TestClient(app)


def test_health() -> None:
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_status_idle() -> None:
    """Test status endpoint when idle."""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == ImportStatus.IDLE


def test_openapi() -> None:
    """Test OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "dhis2-era5land"
