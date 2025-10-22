import io
import os
import re

import pytest
from fastapi import UploadFile
from starlette.datastructures import Headers

from src.uploads.service import UploadsService


@pytest.mark.asyncio
async def test_save_photo_success(local_storage, mock_upload_file):
    service = UploadsService(local_storage)

    path = await service.save_file(mock_upload_file, content_type_prefix="image/")

    assert os.path.exists(path)
    assert re.search(r"test_uploads/.+\.jpg$", path)


@pytest.mark.asyncio
async def test_save_photo_validates_content_type(local_storage):
    service = UploadsService(local_storage)
    fake_text = UploadFile(
        filename="note.txt",
        file=io.BytesIO(b"hello"),
        headers=Headers({"content-type": "text/plain"}),
    )

    with pytest.raises(ValueError) as exc:
        await service.save_file(fake_text, content_type_prefix="image/")

    assert "File must be of type image/" in str(exc.value)


@pytest.mark.asyncio
async def test_delete_photo_success(local_storage, mock_upload_file):
    service = UploadsService(local_storage)
    path = await service.save_file(mock_upload_file, content_type_prefix="image/")
    filename = os.path.basename(path)

    deleted = await service.delete_file(filename)

    assert deleted is True
    assert not os.path.exists(path)


@pytest.mark.asyncio
async def test_delete_photo_failure(local_storage):
    service = UploadsService(local_storage)

    deleted = await service.delete_file("nonexistent.jpg")

    assert deleted is False
