import shutil
from pathlib import Path

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient
from starlette.datastructures import Headers

from app.services.storage.local_storage import LocalFileStorage
from main import app


@pytest.fixture
def client():
    """Creates a TestClient instance for API testing"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_upload_dir():
    """Creates a temporary upload directory for tests"""
    test_dir = Path("test_uploads")
    test_dir.mkdir(exist_ok=True)
    yield test_dir

    if test_dir.exists():
        shutil.rmtree(test_dir)


@pytest.fixture
def local_storage(test_upload_dir):
    """Creates a LocalFileStorage instance with test directory"""
    return LocalFileStorage(upload_dir=str(test_upload_dir))


@pytest.fixture
def mock_upload_file(tmp_path):
    """Creates a mock UploadFile for testing"""
    test_content = b"test image content"
    test_file = tmp_path / "test.jpg"
    test_file.write_bytes(test_content)

    return UploadFile(
        filename="test.jpg",
        file=open(test_file, "rb"),
        headers=Headers({"content-type": "image/jpeg"}),
    )
