"""
Tests for the PhotosService
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import UploadFile

from src.photos.models import SummitPhoto, SummitPhotoCreate
from src.photos.repository import PhotosRepository
from src.photos.service import PhotosService
from src.uploads.service import UploadsService


@pytest.fixture
def mock_uploads_service():
    """Create a mock upload service"""
    service = AsyncMock(spec=UploadsService)
    service.save_file.return_value = "/uploads/test-photo.jpg"
    service.delete_file.return_value = True
    return service


@pytest.fixture
def mock_photos_repository():
    """Create a mock photo repository"""
    repo = MagicMock(spec=PhotosRepository)

    def save_photo(photo):
        photo.id = 1
        return photo

    repo.save.side_effect = save_photo
    repo.get_by_id.return_value = SummitPhoto(id=1, file_name="test-photo.jpg")
    repo.delete.return_value = True
    return repo


@pytest.fixture
def photos_service(
    mock_uploads_service,
    mock_photos_repository,
):
    """Create a PhotosService with mocked dependencies"""
    return PhotosService(
        mock_uploads_service,
        mock_photos_repository,
    )


@pytest.fixture
def mock_file():
    """Create a mock file upload"""
    file = AsyncMock(spec=UploadFile)
    file.filename = "test-photo.jpg"
    file.content_type = "image/jpeg"
    return file


@pytest.mark.asyncio
async def test_upload_photo_with_metadata(
    photos_service,
    mock_file,
    mock_uploads_service,
    mock_photos_repository,
    peak_coords,
):
    """Test uploading a photo with provided metadata"""
    summit_photo_create = SummitPhotoCreate(
        captured_at=datetime(2025, 10, 6, 14, 30, 0),
        latitude=peak_coords["near_rysy"][0],
        longitude=peak_coords["near_rysy"][1],
        altitude=2450.0,
        peak_id=1,
    )

    result = await photos_service.upload_photo(mock_file, summit_photo_create)

    assert result.id == 1
    assert result.file_name == "test-photo.jpg"
    assert result.peak_id == 1
    assert result.distance_to_peak is None
    assert result.captured_at == datetime(2025, 10, 6, 14, 30, 0)
    assert result.altitude == 2450.0
    assert result.latitude == peak_coords["near_rysy"][0]
    assert result.longitude == peak_coords["near_rysy"][1]

    mock_uploads_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_photos_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_upload_photo_without_metadata(
    photos_service,
    mock_file,
    mock_uploads_service,
    mock_photos_repository,
):
    """Test uploading a photo without any metadata"""
    summit_photo_create = SummitPhotoCreate()

    result = await photos_service.upload_photo(mock_file, summit_photo_create)

    assert result.id == 1
    assert result.file_name == "test-photo.jpg"
    assert result.peak_id is None
    assert result.distance_to_peak is None
    assert result.captured_at is None
    assert result.altitude is None
    assert result.latitude is None
    assert result.longitude is None

    mock_uploads_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_photos_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_upload_photo_with_partial_metadata(
    photos_service,
    mock_file,
    mock_uploads_service,
    mock_photos_repository,
):
    """Test uploading a photo with only some metadata fields"""
    summit_photo_create = SummitPhotoCreate(
        captured_at=datetime(2025, 10, 6, 16, 45, 20),
        altitude=1500.0,
    )

    result = await photos_service.upload_photo(mock_file, summit_photo_create)

    assert result.id == 1
    assert result.file_name == "test-photo.jpg"
    assert result.peak_id is None
    assert result.distance_to_peak is None
    assert result.captured_at == datetime(2025, 10, 6, 16, 45, 20)
    assert result.altitude == 1500.0
    assert result.latitude is None
    assert result.longitude is None

    mock_uploads_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_photos_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_get_photo_by_id(photos_service, mock_photos_repository):
    """Test getting a photo by ID"""
    photo_id = 1
    test_photo = SummitPhoto(
        id=photo_id,
        file_name="specific-photo.jpg",
        latitude=49.1794,
        longitude=20.0880,
    )
    mock_photos_repository.get_by_id.return_value = test_photo

    result = await photos_service.get_photo_by_id(photo_id)

    assert result == test_photo
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)


@pytest.mark.asyncio
async def test_get_photo_by_id_not_found(photos_service, mock_photos_repository):
    """Test getting a photo by ID when it doesn't exist"""
    photo_id = 999
    mock_photos_repository.get_by_id.return_value = None

    result = await photos_service.get_photo_by_id(photo_id)

    assert result is None
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)


@pytest.mark.asyncio
async def test_get_all_photos(photos_service, mock_photos_repository):
    """Test getting all photos"""
    test_photos = [
        SummitPhoto(id=1, file_name="test1.jpg"),
        SummitPhoto(id=2, file_name="test2.jpg"),
    ]
    mock_photos_repository.get_all.return_value = test_photos

    result = await photos_service.get_all_photos()

    assert result == test_photos
    mock_photos_repository.get_all.assert_called_once_with(sort_by=None, order=None)


@pytest.mark.asyncio
async def test_delete_photo_success(
    photos_service, mock_uploads_service, mock_photos_repository
):
    """Test deleting a photo successfully"""
    photo_id = 1
    result = await photos_service.delete_photo(photo_id)

    assert result is True
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)
    mock_uploads_service.delete_file.assert_called_once_with("test-photo.jpg")
    mock_photos_repository.delete.assert_called_once_with(photo_id)


@pytest.mark.asyncio
async def test_delete_photo_failure_no_file(
    photos_service, mock_uploads_service, mock_photos_repository
):
    """Test deleting a photo when the file deletion fails"""
    photo_id = 1
    mock_uploads_service.delete_file.return_value = False

    result = await photos_service.delete_photo(photo_id)

    assert result is False
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)
    mock_uploads_service.delete_file.assert_called_once_with("test-photo.jpg")
    mock_photos_repository.delete.assert_not_called()


@pytest.mark.asyncio
async def test_delete_photo_failure_not_found(photos_service, mock_photos_repository):
    """Test deleting a photo that doesn't exist"""
    photo_id = 999
    mock_photos_repository.get_by_id.return_value = None

    result = await photos_service.delete_photo(photo_id)

    assert result is False
    mock_photos_repository.get_by_id.assert_called_once_with(photo_id)
    mock_photos_repository.delete.assert_not_called()
