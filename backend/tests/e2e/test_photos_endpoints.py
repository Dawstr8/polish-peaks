import os
import re
from datetime import datetime
from pathlib import Path

import pytest

from main import app
from src.photos import dependencies
from src.photos.services.metadata_extractor import MetadataExtractorInterface
from src.uploads.service import UploadService
from src.uploads.services.local_storage import LocalFileStorage
from tests.fixtures.peak_fixtures import peak_coords_dms


class MockMetadataExtractor(MetadataExtractorInterface):
    """Mock metadata extractor for testing"""

    def __init__(self, metadata=None):
        self.metadata = metadata or {}

    def extract(self, path: str):
        return self.metadata


@pytest.fixture(autouse=True)
def override_upload_service(test_upload_dir):
    """Override the upload service dependency to isolate filesystem writes."""

    def _get_upload_service():
        return UploadService(LocalFileStorage(upload_dir=str(test_upload_dir)))

    app.dependency_overrides[dependencies.get_upload_service] = _get_upload_service
    yield
    app.dependency_overrides.pop(dependencies.get_upload_service, None)


def test_get_all_photos_empty(client_with_db):
    """Test getting all photos when none exist"""
    resp = client_with_db.get("/api/photos/")

    assert resp.status_code == 200
    assert resp.json() == []


def test_get_all_photos(client_with_db):
    """Test getting all photos"""

    def _get_metadata_extractor():
        return MockMetadataExtractor({})

    app.dependency_overrides[dependencies.get_metadata_extractor] = (
        _get_metadata_extractor
    )

    try:
        client_with_db.post(
            "/api/photos/",
            files={"file": ("photo1.jpg", b"imagedata1", "image/jpeg")},
        )

        client_with_db.post(
            "/api/photos/",
            files={"file": ("photo2.jpg", b"imagedata2", "image/jpeg")},
        )

        resp = client_with_db.get("/api/photos/")

        assert resp.status_code == 200
        photos = resp.json()
        assert len(photos) >= 2

        for photo in photos:
            assert "id" in photo
            assert "file_name" in photo

    finally:
        app.dependency_overrides.pop(dependencies.get_metadata_extractor, None)


def test_upload_photo_success(client_with_db):
    """Test successful photo upload"""
    metadata = {
        "captured_at": "2025:10:06 14:30:00",
        "gps_latitude": (49, 10, 0),
        "gps_longitude": (20, 5, 0),
        "gps_altitude": 2000.0,
    }

    def _get_metadata_extractor():
        return MockMetadataExtractor(metadata)

    app.dependency_overrides[dependencies.get_metadata_extractor] = (
        _get_metadata_extractor
    )

    try:
        resp = client_with_db.post(
            "/api/photos/",
            files={"file": ("summit.jpg", b"binaryimagedata", "image/jpeg")},
        )

        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["id"] is not None
        assert re.search(r".+\.jpg$", data["file_name"])
        assert Path(f"test_uploads/{data['file_name']}").exists()
    finally:
        app.dependency_overrides.pop(dependencies.get_metadata_extractor, None)


def test_upload_invalid_file_type(client_with_db):
    """Test upload with invalid file type"""
    resp = client_with_db.post(
        "/api/photos/",
        files={"file": ("notes.txt", b"not an image", "text/plain")},
    )

    assert resp.status_code == 400
    assert resp.json()["detail"] == "File must be of type image/"


def test_upload_with_matching_peak(client_with_db, test_peaks, peak_coords_dms):
    """Test upload photo with GPS coordinates that match to a nearby peak"""
    metadata = {
        "captured_at": "2025:10:06 14:30:00",
        "gps_latitude": peak_coords_dms["near_rysy"][0],
        "gps_longitude": peak_coords_dms["near_rysy"][1],
        "gps_altitude": 2450.0,
    }

    def _get_metadata_extractor():
        return MockMetadataExtractor(metadata)

    app.dependency_overrides[dependencies.get_metadata_extractor] = (
        _get_metadata_extractor
    )

    try:
        resp = client_with_db.post(
            "/api/photos/",
            files={"file": ("mountain_photo.jpg", b"binaryimagedata", "image/jpeg")},
        )

        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["id"] is not None
        assert data["file_name"] is not None

        assert data["latitude"] is not None
        assert data["longitude"] is not None
        assert data["altitude"] == metadata["gps_altitude"]

        assert data["peak_id"] is not None
        assert data["distance_to_peak"] is not None
        assert data["distance_to_peak"] < 20

    finally:
        app.dependency_overrides.pop(dependencies.get_metadata_extractor, None)


def test_upload_with_no_matching_peak(client_with_db, test_peaks, peak_coords_dms):
    """Test upload photo with GPS coordinates that don't match any peak"""

    metadata = {
        "captured_at": "2025:10:06 14:30:00",
        "gps_latitude": peak_coords_dms["warsaw"][0],
        "gps_longitude": peak_coords_dms["warsaw"][1],
        "gps_altitude": 120.0,
    }

    def _get_metadata_extractor():
        return MockMetadataExtractor(metadata)

    app.dependency_overrides[dependencies.get_metadata_extractor] = (
        _get_metadata_extractor
    )

    try:
        resp = client_with_db.post(
            "/api/photos/",
            files={"file": ("city_photo.jpg", b"binaryimagedata", "image/jpeg")},
        )

        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["id"] is not None
        assert data["file_name"] is not None

        assert data["latitude"] is not None
        assert data["longitude"] is not None
        assert data["altitude"] == metadata["gps_altitude"]

        assert data["peak_id"] is None
        assert data["distance_to_peak"] is None

    finally:
        app.dependency_overrides.pop(dependencies.get_metadata_extractor, None)


def test_upload_without_gps_data(client_with_db, test_peaks):
    """Test upload photo without GPS coordinates"""

    metadata = {
        "captured_at": "2025:10:06 14:30:00",
        "gps_latitude": None,
        "gps_longitude": None,
        "gps_altitude": None,
    }

    def _get_metadata_extractor():
        return MockMetadataExtractor(metadata)

    app.dependency_overrides[dependencies.get_metadata_extractor] = (
        _get_metadata_extractor
    )

    try:
        resp = client_with_db.post(
            "/api/photos/",
            files={"file": ("indoor_photo.jpg", b"binaryimagedata", "image/jpeg")},
        )

        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["id"] is not None
        assert data["file_name"] is not None

        assert data["latitude"] is None
        assert data["longitude"] is None
        assert data["altitude"] is None

        assert data["peak_id"] is None
        assert data["distance_to_peak"] is None

    finally:
        app.dependency_overrides.pop(dependencies.get_metadata_extractor, None)


def test_get_photo_by_id(client_with_db):
    """Test getting a specific photo by ID"""

    def _get_metadata_extractor():
        return MockMetadataExtractor({})

    app.dependency_overrides[dependencies.get_metadata_extractor] = (
        _get_metadata_extractor
    )

    try:
        upload_resp = client_with_db.post(
            "/api/photos/",
            files={"file": ("specific_photo.jpg", b"specificimagedata", "image/jpeg")},
        )

        upload_data = upload_resp.json()
        photo_id = upload_data["id"]

        get_resp = client_with_db.get(f"/api/photos/{photo_id}")

        assert get_resp.status_code == 200
        photo_data = get_resp.json()

        assert photo_data["id"] == photo_id
        assert photo_data["file_name"] == upload_data["file_name"]

    finally:
        app.dependency_overrides.pop(dependencies.get_metadata_extractor, None)


def test_get_nonexistent_photo(client_with_db):
    """Test getting a photo that doesn't exist"""
    resp = client_with_db.get("/api/photos/9999")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Photo not found"


def test_delete_photo_success(client_with_db):
    """Test deleting a photo successfully"""
    upload = client_with_db.post(
        "/api/photos/",
        files={"file": ("delete_me.jpg", b"imagedata", "image/jpeg")},
    )
    photo_data = upload.json()
    photo_id = photo_data["id"]
    file_path = f"test_uploads/{photo_data['file_name']}"

    delete_resp = client_with_db.delete(f"/api/photos/{photo_id}")

    assert delete_resp.status_code == 200
    assert delete_resp.json()["success"] is True
    assert not os.path.exists(file_path)


def test_delete_nonexistent_photo(client_with_db):
    """Test deleting a photo that doesn't exist"""
    resp = client_with_db.delete("/api/photos/9999")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Photo not found"
