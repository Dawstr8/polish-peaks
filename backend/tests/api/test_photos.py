import os
import re
from pathlib import Path

import pytest

from app.api.endpoints import photos
from app.services.photo_service import PhotoService
from app.services.storage.local_storage import LocalFileStorage
from main import app


@pytest.fixture(autouse=True)
def override_photo_dependency(test_upload_dir):
    """Override the photo service dependency to isolate filesystem writes."""

    def _get_service():
        return PhotoService(LocalFileStorage(upload_dir=str(test_upload_dir)))

    app.dependency_overrides[photos.get_photo_service] = _get_service
    yield
    app.dependency_overrides.pop(photos.get_photo_service, None)


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
    assert resp.json()["detail"] == "File must be a photo"


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
