"""
Tests for the PhotoService
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import UploadFile

from src.common.utils.geo import dms_to_decimal
from src.peaks.model import Peak
from src.peaks.service import PeakService
from src.photos.model import SummitPhoto
from src.photos.repository import PhotoRepository
from src.photos.service import PhotoService
from src.photos.services.metadata_extractor import MetadataExtractorInterface
from src.uploads.service import UploadService


@pytest.fixture
def mock_upload_service():
    """Create a mock upload service"""
    service = AsyncMock(spec=UploadService)
    service.save_file.return_value = "/uploads/test-photo.jpg"
    service.delete_file.return_value = True
    return service


@pytest.fixture
def mock_metadata_extractor():
    """Create a mock metadata extractor"""
    extractor = MagicMock(spec=MetadataExtractorInterface)
    return extractor


@pytest.fixture
def mock_peak_service():
    """Create a mock peak service"""
    service = MagicMock(spec=PeakService)
    return service


@pytest.fixture
def mock_photo_repository():
    """Create a mock photo repository"""
    repo = MagicMock(spec=PhotoRepository)

    def save_photo(photo):
        photo.id = 1
        return photo

    repo.save.side_effect = save_photo
    repo.get_by_id.return_value = SummitPhoto(id=1, file_name="test-photo.jpg")
    repo.delete.return_value = True
    return repo


@pytest.fixture
def photo_service(
    mock_upload_service,
    mock_metadata_extractor,
    mock_peak_service,
    mock_photo_repository,
):
    """Create a PhotoService with mocked dependencies"""
    return PhotoService(
        mock_upload_service,
        mock_metadata_extractor,
        mock_peak_service,
        mock_photo_repository,
    )


@pytest.fixture
def mock_file():
    """Create a mock file upload"""
    file = AsyncMock(spec=UploadFile)
    file.filename = "test-photo.jpg"
    file.content_type = "image/jpeg"
    return file


@pytest.mark.asyncio
async def test_process_photo_upload_with_matching_peak(
    photo_service,
    mock_file,
    mock_upload_service,
    mock_metadata_extractor,
    mock_peak_service,
    mock_photo_repository,
    peak_coords,
    peak_coords_dms,
):
    """Test processing a photo upload with matching peak"""
    metadata = {
        "captured_at": "2025:10:06 14:30:00",
        "gps_latitude": peak_coords_dms["near_rysy"][0],
        "gps_longitude": peak_coords_dms["near_rysy"][1],
        "gps_altitude": 2450.0,
    }
    mock_metadata_extractor.extract.return_value = metadata

    rysy = Peak(
        id=1,
        name="Rysy",
        elevation=2499,
        latitude=49.1795,
        longitude=20.0881,
        range="Tatry",
    )
    distance = 15.5
    mock_peak_service.find_nearest_peaks.return_value = [
        {"peak": rysy, "distance": distance}
    ]

    result = await photo_service.process_photo_upload(mock_file)

    assert result.id == 1
    assert result.file_name == "test-photo.jpg"
    assert result.peak_id == 1
    assert result.distance_to_peak == distance
    assert result.captured_at == datetime(2025, 10, 6, 14, 30, 0)
    assert result.altitude == 2450.0
    assert result.latitude == peak_coords["near_rysy"][0]
    assert result.longitude == peak_coords["near_rysy"][1]

    mock_upload_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_metadata_extractor.extract.assert_called_once_with("/uploads/test-photo.jpg")
    mock_peak_service.find_nearest_peaks.assert_called_once_with(
        latitude=dms_to_decimal(metadata["gps_latitude"]),
        longitude=dms_to_decimal(metadata["gps_longitude"]),
        limit=1,
    )
    mock_photo_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_process_photo_upload_no_matching_peak(
    photo_service,
    mock_file,
    mock_upload_service,
    mock_metadata_extractor,
    mock_peak_service,
    mock_photo_repository,
    peak_coords,
    peak_coords_dms,
):
    """Test processing a photo upload with no matching peak"""
    metadata = {
        "captured_at": "2025:10:06 14:30:00",
        "gps_latitude": peak_coords_dms["warsaw"][0],
        "gps_longitude": peak_coords_dms["warsaw"][1],
        "gps_altitude": 120.0,
    }
    mock_metadata_extractor.extract.return_value = metadata

    mock_peak_service.find_nearest_peaks.return_value = []

    result = await photo_service.process_photo_upload(mock_file)

    assert result.id == 1
    assert result.file_name == "test-photo.jpg"
    assert result.peak_id is None
    assert result.distance_to_peak is None
    assert result.captured_at == datetime(2025, 10, 6, 14, 30, 0)
    assert result.altitude == 120.0
    assert result.latitude == peak_coords["warsaw"][0]
    assert result.longitude == peak_coords["warsaw"][1]

    mock_upload_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_metadata_extractor.extract.assert_called_once_with("/uploads/test-photo.jpg")
    mock_peak_service.find_nearest_peaks.assert_called_once()
    mock_photo_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_process_photo_upload_without_gps_data(
    photo_service,
    mock_file,
    mock_upload_service,
    mock_metadata_extractor,
    mock_peak_service,
    mock_photo_repository,
):
    """Test processing a photo upload without GPS data"""
    metadata = {
        "captured_at": "2025:10:06 16:45:20",
        "gps_altitude": None,
    }
    mock_metadata_extractor.extract.return_value = metadata

    result = await photo_service.process_photo_upload(mock_file)

    assert result.id == 1
    assert result.file_name == "test-photo.jpg"
    assert result.peak_id is None
    assert result.distance_to_peak is None
    assert result.captured_at == datetime(2025, 10, 6, 16, 45, 20)
    assert result.altitude is None
    assert result.latitude is None
    assert result.longitude is None

    mock_upload_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_metadata_extractor.extract.assert_called_once_with("/uploads/test-photo.jpg")
    mock_peak_service.find_nearest_peaks.assert_not_called()
    mock_photo_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_process_photo_upload_without_metadata(
    photo_service,
    mock_file,
    mock_upload_service,
    mock_metadata_extractor,
    mock_peak_service,
    mock_photo_repository,
):
    """Test processing a photo upload without metadata"""
    metadata = {
        "captured_at": None,
        "gps_latitude": None,
        "gps_longitude": None,
        "gps_altitude": None,
    }
    mock_metadata_extractor.extract.return_value = metadata

    result = await photo_service.process_photo_upload(mock_file)

    assert result.id == 1
    assert result.file_name == "test-photo.jpg"
    assert result.peak_id is None
    assert result.distance_to_peak is None
    assert result.captured_at is None
    assert result.altitude is None
    assert result.latitude is None
    assert result.longitude is None

    mock_upload_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_metadata_extractor.extract.assert_called_once_with("/uploads/test-photo.jpg")
    mock_peak_service.find_nearest_peaks.assert_not_called()
    mock_photo_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_get_photo_by_id(photo_service, mock_photo_repository):
    """Test getting a photo by ID"""
    photo_id = 1
    test_photo = SummitPhoto(
        id=photo_id,
        file_name="specific-photo.jpg",
        latitude=49.1794,
        longitude=20.0880,
    )
    mock_photo_repository.get_by_id.return_value = test_photo

    result = await photo_service.get_photo_by_id(photo_id)

    assert result == test_photo
    mock_photo_repository.get_by_id.assert_called_once_with(photo_id)


@pytest.mark.asyncio
async def test_get_photo_by_id_not_found(photo_service, mock_photo_repository):
    """Test getting a photo by ID when it doesn't exist"""
    photo_id = 999
    mock_photo_repository.get_by_id.return_value = None

    result = await photo_service.get_photo_by_id(photo_id)

    assert result is None
    mock_photo_repository.get_by_id.assert_called_once_with(photo_id)


@pytest.mark.asyncio
async def test_get_all_photos(photo_service, mock_photo_repository):
    """Test getting all photos"""
    test_photos = [
        SummitPhoto(id=1, file_name="test1.jpg"),
        SummitPhoto(id=2, file_name="test2.jpg"),
    ]
    mock_photo_repository.get_all.return_value = test_photos

    result = await photo_service.get_all_photos()

    assert result == test_photos
    mock_photo_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_delete_photo_success(
    photo_service, mock_upload_service, mock_photo_repository
):
    """Test deleting a photo successfully"""
    photo_id = 1
    result = await photo_service.delete_photo(photo_id)

    assert result is True
    mock_photo_repository.get_by_id.assert_called_once_with(photo_id)
    mock_upload_service.delete_file.assert_called_once_with("test-photo.jpg")
    mock_photo_repository.delete.assert_called_once_with(photo_id)


@pytest.mark.asyncio
async def test_delete_photo_failure_no_file(
    photo_service, mock_upload_service, mock_photo_repository
):
    """Test deleting a photo when the file deletion fails"""
    photo_id = 1
    mock_upload_service.delete_file.return_value = False

    result = await photo_service.delete_photo(photo_id)

    assert result is False
    mock_photo_repository.get_by_id.assert_called_once_with(photo_id)
    mock_upload_service.delete_file.assert_called_once_with("test-photo.jpg")
    mock_photo_repository.delete.assert_not_called()


@pytest.mark.asyncio
async def test_delete_photo_failure_not_found(photo_service, mock_photo_repository):
    """Test deleting a photo that doesn't exist"""
    photo_id = 999
    mock_photo_repository.get_by_id.return_value = None

    result = await photo_service.delete_photo(photo_id)

    assert result is False
    mock_photo_repository.get_by_id.assert_called_once_with(photo_id)
    mock_photo_repository.delete.assert_not_called()
