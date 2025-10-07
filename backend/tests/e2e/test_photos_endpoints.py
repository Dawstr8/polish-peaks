import os
import re
from pathlib import Path

import pytest

from main import app
from src.photos import dependencies
from src.photos.services.metadata_extractor import MetadataExtractorInterface
from src.uploads.service import UploadService
from src.uploads.services.local_storage import LocalFileStorage


class MockMetadataExtractor(MetadataExtractorInterface):
    """Mock metadata extractor for testing"""

    def __init__(self, metadata=None):
        self.metadata = metadata or {}

    def extract(self, path: str):
        return self.metadata


@pytest.fixture(autouse=True)
def override_photo_dependency(test_upload_dir):
    """Override the photo service dependency to isolate filesystem writes."""

    def _get_upload_service():
        return UploadService(LocalFileStorage(upload_dir=str(test_upload_dir)))

    app.dependency_overrides[dependencies.get_upload_service] = _get_upload_service
    yield
    app.dependency_overrides.pop(dependencies.get_upload_service, None)


def test_upload_photo_success(client):
    resp = client.post(
        "/api/photos/upload",
        files={"file": ("summit.jpg", b"binaryimagedata", "image/jpeg")},
    )

    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["success"] is True
    assert re.search(r"test_uploads/.+\.jpg$", data["path"])
    assert Path(data["path"]).exists()


def test_upload_invalid_file_type(client):
    resp = client.post(
        "/api/photos/upload",
        files={"file": ("notes.txt", b"not an image", "text/plain")},
    )

    assert resp.status_code == 400
    assert resp.json()["detail"] == "File must be of type image/"


def test_upload_with_matching_peak(client_with_db, test_peaks):
    """Test upload photo with GPS coordinates that match to a nearby peak"""

    # Coordinates near Rysy peak
    dms_lat = (49, 10, 45.84)
    dms_lon = (20, 5, 16.8)

    metadata = {
        "captured_at": "2025:10:06 10:15:29",
        "gps_latitude": dms_lat,
        "gps_longitude": dms_lon,
        "gps_altitude": 2450.0,
    }

    def _get_metadata_extractor():
        return MockMetadataExtractor(metadata)

    app.dependency_overrides[dependencies.get_metadata_extractor] = (
        _get_metadata_extractor
    )

    try:
        resp = client_with_db.post(
            "/api/photos/upload",
            files={"file": ("mountain_photo.jpg", b"binaryimagedata", "image/jpeg")},
        )

        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["success"] is True
        assert "path" in data

        assert data["metadata"]["captured_at"] == metadata["captured_at"]
        assert data["metadata"]["gps_altitude"] == metadata["gps_altitude"]

        assert len(data["metadata"]["gps_latitude"]) == 3
        assert len(data["metadata"]["gps_longitude"]) == 3
        for i in range(3):
            assert data["metadata"]["gps_latitude"][i] == metadata["gps_latitude"][i]
            assert data["metadata"]["gps_longitude"][i] == metadata["gps_longitude"][i]

        assert data["matched_peak"] is not None
        assert data["matched_peak"]["name"] == "Rysy"
        assert data["matched_peak"]["elevation"] == 2499
        assert data["matched_peak"]["range"] == "Tatry"
        assert data["matched_peak"]["distance_m"] < 20

    finally:
        app.dependency_overrides.pop(dependencies.get_metadata_extractor, None)


def test_upload_with_no_matching_peak(client_with_db, test_peaks):
    """Test upload photo with GPS coordinates that don't match any peak"""

    # Coordinates in Warsaw, far from any peak
    dms_lat = (52, 13, 46.92)
    dms_lon = (21, 0, 43.92)

    metadata = {
        "captured_at": "2025:10:06 14:30:00",
        "gps_latitude": dms_lat,
        "gps_longitude": dms_lon,
        "gps_altitude": 120.0,
    }

    def _get_metadata_extractor():
        return MockMetadataExtractor(metadata)

    app.dependency_overrides[dependencies.get_metadata_extractor] = (
        _get_metadata_extractor
    )

    try:
        # Upload photo
        resp = client_with_db.post(
            "/api/photos/upload",
            files={"file": ("city_photo.jpg", b"binaryimagedata", "image/jpeg")},
        )

        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["success"] is True
        assert "path" in data

        assert data["metadata"]["captured_at"] == metadata["captured_at"]
        assert data["metadata"]["gps_altitude"] == metadata["gps_altitude"]

        assert len(data["metadata"]["gps_latitude"]) == 3
        assert len(data["metadata"]["gps_longitude"]) == 3
        for i in range(3):
            assert data["metadata"]["gps_latitude"][i] == metadata["gps_latitude"][i]
            assert data["metadata"]["gps_longitude"][i] == metadata["gps_longitude"][i]

        assert data["matched_peak"] is None

    finally:
        app.dependency_overrides.pop(dependencies.get_metadata_extractor, None)


def test_upload_without_gps_data(client_with_db):
    """Test upload photo without GPS coordinates"""

    metadata = {
        "captured_at": "2025:10:06 16:45:20",
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
            "/api/photos/upload",
            files={"file": ("indoor_photo.jpg", b"binaryimagedata", "image/jpeg")},
        )

        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["success"] is True
        assert "path" in data

        assert data["metadata"]["captured_at"] == metadata["captured_at"]
        assert data["metadata"]["gps_latitude"] == metadata["gps_latitude"]
        assert data["metadata"]["gps_longitude"] == metadata["gps_longitude"]
        assert data["metadata"]["gps_altitude"] == metadata["gps_altitude"]

        assert data["matched_peak"] is None

    finally:
        app.dependency_overrides.pop(dependencies.get_metadata_extractor, None)


def test_delete_photo_success(client):
    upload = client.post(
        "/api/photos/upload",
        files={"file": ("delete_me.jpg", b"imagedata", "image/jpeg")},
    )
    path = upload.json()["path"]
    filename = os.path.basename(path)

    delete_resp = client.delete(f"/api/photos/{filename}")

    assert delete_resp.status_code == 200
    assert delete_resp.json()["success"] is True
    assert not os.path.exists(path)


def test_delete_nonexistent_photo(client):
    resp = client.delete("/api/photos/does_not_exist.jpg")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Photo not found"
