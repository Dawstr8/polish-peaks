import os

import pytest

from app.services.storage.local_storage import LocalFileStorage


@pytest.mark.asyncio
async def test_local_storage_creates_directory(tmp_path):
    target_dir = tmp_path / "nested_uploads"
    LocalFileStorage(upload_dir=str(target_dir))
    assert target_dir.exists() and target_dir.is_dir()


@pytest.mark.asyncio
async def test_local_storage_save_file(local_storage, mock_upload_file):
    saved_path = await local_storage.save_file(mock_upload_file, "example.jpg")

    assert os.path.exists(saved_path)
    with open(saved_path, "rb") as f:
        assert f.read() == b"test image content"


@pytest.mark.asyncio
async def test_local_storage_delete_file(local_storage, mock_upload_file):
    path = await local_storage.save_file(mock_upload_file, "todelete.jpg")
    filename = os.path.basename(path)

    deleted = await local_storage.delete_file(filename)

    assert deleted is True
    assert not os.path.exists(path)


@pytest.mark.asyncio
async def test_local_storage_delete_nonexistent_file(local_storage):
    deleted = await local_storage.delete_file("missing.jpg")

    assert deleted is False
