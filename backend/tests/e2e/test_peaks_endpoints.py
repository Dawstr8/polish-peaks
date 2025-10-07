import pytest
from fastapi.testclient import TestClient

from src.peaks.model import Peak


def test_get_peaks(client_with_db: TestClient, test_peaks: list[Peak]):
    """Test getting all peaks"""
    response = client_with_db.get("/api/peaks/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    peak_names = [peak["name"] for peak in data]
    expected_names = ["Rysy", "Śnieżka", "Babia Góra"]
    assert all(name in peak_names for name in expected_names)

    for peak in data:
        assert "id" in peak
        assert "name" in peak
        assert "elevation" in peak
        assert "latitude" in peak
        assert "longitude" in peak
        assert "range" in peak
        assert "created_at" in peak


def test_get_peaks_empty_database(client_with_db: TestClient):
    """Test getting peaks when the database is empty"""
    response = client_with_db.get("/api/peaks/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_peak(client_with_db: TestClient, test_peaks: list[Peak]):
    """Test getting a specific peak by ID"""
    peak_id = test_peaks[0].id

    response = client_with_db.get(f"/api/peaks/{peak_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == peak_id
    assert data["name"] == "Rysy"
    assert data["elevation"] == 2499
    assert data["latitude"] == 49.1795
    assert data["longitude"] == 20.0881
    assert data["range"] == "Tatry"
    assert "created_at" in data


def test_get_peak_not_found(client_with_db: TestClient):
    """Test getting a non-existent peak"""
    response = client_with_db.get("/api/peaks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Peak not found"}
