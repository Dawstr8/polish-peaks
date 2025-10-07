"""
Tests for the PhotoService
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import UploadFile

from src.common.utils.geo import dms_to_decimal
from src.peaks.model import Peak
from src.peaks.service import PeakService
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
def photo_service(mock_upload_service, mock_metadata_extractor, mock_peak_service):
    """Create a PhotoService with mocked dependencies"""
    return PhotoService(mock_upload_service, mock_metadata_extractor, mock_peak_service)


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
):
    """Test processing a photo upload with matching peak"""
    near_rysy = [(49, 10, 45.84), (20, 5, 16.8)]
    metadata = {
        "captured_at": "2025:10:06 14:30:00",
        "gps_latitude": near_rysy[0],
        "gps_longitude": near_rysy[1],
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
    mock_peak_service.find_nearest_peak.return_value = (rysy, distance)

    result = await photo_service.process_photo_upload(mock_file)

    assert result["success"] is True
    assert result["path"] == "/uploads/test-photo.jpg"
    assert result["metadata"] == metadata
    assert result["matched_peak"] is not None
    assert result["matched_peak"]["id"] == 1
    assert result["matched_peak"]["name"] == "Rysy"
    assert result["matched_peak"]["elevation"] == 2499
    assert result["matched_peak"]["range"] == "Tatry"
    assert result["matched_peak"]["distance_m"] == round(distance, 2)

    mock_upload_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_metadata_extractor.extract.assert_called_once_with("/uploads/test-photo.jpg")
    mock_peak_service.find_nearest_peak.assert_called_once_with(
        latitude=dms_to_decimal(metadata["gps_latitude"]),
        longitude=dms_to_decimal(metadata["gps_longitude"]),
        max_distance_m=5000.0,
    )


@pytest.mark.asyncio
async def test_process_photo_upload_no_matching_peak(
    photo_service,
    mock_file,
    mock_upload_service,
    mock_metadata_extractor,
    mock_peak_service,
):
    """Test processing a photo upload with no matching peak"""
    warsaw = [(52, 13, 46.92), (21, 0, 43.92)]
    metadata = {
        "captured_at": "2025:10:06 14:30:00",
        "gps_latitude": warsaw[0],
        "gps_longitude": warsaw[1],
        "gps_altitude": 120.0,
    }
    mock_metadata_extractor.extract.return_value = metadata

    mock_peak_service.find_nearest_peak.return_value = None

    result = await photo_service.process_photo_upload(mock_file)

    assert result["success"] is True
    assert result["path"] == "/uploads/test-photo.jpg"
    assert result["metadata"] == metadata
    assert result["matched_peak"] is None

    mock_upload_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_metadata_extractor.extract.assert_called_once_with("/uploads/test-photo.jpg")
    mock_peak_service.find_nearest_peak.assert_called_once()


@pytest.mark.asyncio
async def test_process_photo_upload_without_gps_data(
    photo_service,
    mock_file,
    mock_upload_service,
    mock_metadata_extractor,
    mock_peak_service,
):
    """Test processing a photo upload without GPS data"""
    metadata = {
        "captured_at": "2025:10:06 16:45:20",
        "gps_altitude": None,
    }
    mock_metadata_extractor.extract.return_value = metadata

    result = await photo_service.process_photo_upload(mock_file)

    assert result["success"] is True
    assert result["path"] == "/uploads/test-photo.jpg"
    assert result["metadata"] == metadata
    assert result["matched_peak"] is None

    mock_upload_service.save_file.assert_called_once_with(
        mock_file, content_type_prefix="image/"
    )
    mock_metadata_extractor.extract.assert_called_once_with("/uploads/test-photo.jpg")
    mock_peak_service.find_nearest_peak.assert_not_called()


@pytest.mark.asyncio
async def test_delete_photo_success(photo_service, mock_upload_service):
    """Test deleting a photo successfully"""
    result = await photo_service.delete_photo("test-photo.jpg")

    assert result is True
    mock_upload_service.delete_file.assert_called_once_with("test-photo.jpg")


@pytest.mark.asyncio
async def test_delete_photo_failure(photo_service, mock_upload_service):
    """Test deleting a photo that doesn't exist"""
    mock_upload_service.delete_file.return_value = False

    result = await photo_service.delete_photo("nonexistent.jpg")

    assert result is False
    mock_upload_service.delete_file.assert_called_once_with("nonexistent.jpg")
