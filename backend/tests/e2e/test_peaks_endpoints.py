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


def test_find_nearest_peaks(
    client_with_db: TestClient, test_peaks: list[Peak], peak_coords: dict
):
    """Test finding nearest peaks to a location"""
    response = client_with_db.get(
        "/api/peaks/find",
        params={
            "latitude": peak_coords["near_rysy"][0],
            "longitude": peak_coords["near_rysy"][1],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    for item in data:
        assert "peak" in item
        assert "distance" in item
        assert isinstance(item["distance"], (int, float))
        assert item["distance"] >= 0

        peak = item["peak"]
        assert "id" in peak
        assert "name" in peak
        assert "elevation" in peak
        assert "latitude" in peak
        assert "longitude" in peak
        assert "range" in peak

    distances = [item["distance"] for item in data]
    assert distances == sorted(distances)

    assert data[0]["peak"]["name"] == "Rysy"
    assert data[0]["distance"] < 100


def test_find_nearest_peaks_with_limit(
    client_with_db: TestClient, test_peaks: list[Peak], peak_coords: dict
):
    """Test finding nearest peaks with a custom limit"""
    response = client_with_db.get(
        "/api/peaks/find",
        params={
            "latitude": peak_coords["near_rysy"][0],
            "longitude": peak_coords["near_rysy"][1],
            "limit": 2,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    assert data[0]["distance"] < data[1]["distance"]
    assert data[0]["peak"]["name"] == "Rysy"


def test_find_nearest_peaks_from_sniezka(
    client_with_db: TestClient, test_peaks: list[Peak], peak_coords: dict
):
    """Test finding nearest peaks from coordinates near Śnieżka"""
    response = client_with_db.get(
        "/api/peaks/find",
        params={
            "latitude": peak_coords["near_sniezka"][0],
            "longitude": peak_coords["near_sniezka"][1],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    assert data[0]["peak"]["name"] == "Śnieżka"
    assert data[0]["distance"] < 100


def test_find_nearest_peaks_empty_database(
    client_with_db: TestClient, peak_coords: dict
):
    """Test finding nearest peaks when the database is empty"""
    response = client_with_db.get(
        "/api/peaks/find",
        params={
            "latitude": peak_coords["near_rysy"][0],
            "longitude": peak_coords["near_rysy"][1],
        },
    )

    assert response.status_code == 200
    assert response.json() == []


def test_find_nearest_peaks_missing_parameters(
    client_with_db: TestClient, peak_coords: dict
):
    """Test that missing required parameters return an error"""
    response = client_with_db.get(
        "/api/peaks/find", params={"latitude": peak_coords["near_rysy"][0]}
    )

    assert response.status_code == 422

    response = client_with_db.get(
        "/api/peaks/find", params={"longitude": peak_coords["near_rysy"][1]}
    )

    assert response.status_code == 422

    response = client_with_db.get("/api/peaks/find")

    assert response.status_code == 422


def test_find_nearest_peaks_invalid_parameters(
    client_with_db: TestClient, peak_coords: dict
):
    """Test that invalid parameters return an error"""
    response = client_with_db.get(
        "/api/peaks/find",
        params={"latitude": "invalid", "longitude": peak_coords["near_rysy"][1]},
    )

    assert response.status_code == 422

    response = client_with_db.get(
        "/api/peaks/find",
        params={
            "latitude": peak_coords["near_rysy"][0],
            "longitude": peak_coords["near_rysy"][1],
            "limit": "invalid",
        },
    )

    assert response.status_code == 422


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
