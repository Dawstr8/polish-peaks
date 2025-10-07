import os
import tempfile
from unittest.mock import mock_open, patch

import pytest

from src.photos.services.exif_metadata_extractor import ExifMetadataExtractor


class MockExifImage:
    """A mock implementation of ExifImage for testing"""

    def __init__(self, has_exif=True, data=None):
        self.has_exif = has_exif
        self._data = data or {}

        if has_exif:
            self.datetime_original = "2023:10:15 14:30:45"
            self.gps_latitude = (50.12345, 0, 0)
            self.gps_longitude = (19.98765, 0, 0)
            self.gps_altitude = 1200.5


@pytest.fixture
def image_path():
    """Returns a path to a mock image"""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
        tmp_file.write(b"Mock image")
        path = tmp_file.name

    yield path

    if os.path.exists(path):
        os.unlink(path)


def test_extract_with_exif_data(image_path):
    """Test extraction when EXIF data is available"""
    extractor = ExifMetadataExtractor()

    with patch(
        "src.photos.services.exif_metadata_extractor.ExifImage",
        return_value=MockExifImage(has_exif=True),
    ):
        metadata = extractor.extract(image_path)

    assert metadata["captured_at"] == "2023:10:15 14:30:45"
    assert metadata["gps_latitude"] == (50.12345, 0, 0)
    assert metadata["gps_longitude"] == (19.98765, 0, 0)
    assert metadata["gps_altitude"] == 1200.5


def test_extract_without_exif_data(image_path):
    """Test extraction when no EXIF data is available"""
    extractor = ExifMetadataExtractor()

    with patch(
        "src.photos.services.exif_metadata_extractor.ExifImage",
        return_value=MockExifImage(has_exif=False),
    ):
        metadata = extractor.extract(image_path)

    assert metadata["captured_at"] is None
    assert metadata["gps_latitude"] is None
    assert metadata["gps_longitude"] is None
    assert metadata["gps_altitude"] is None


def test_extract_with_nonexistent_file():
    """Test extraction with a file that doesn't exist"""
    extractor = ExifMetadataExtractor()

    with patch("builtins.open", side_effect=FileNotFoundError):
        metadata = extractor.extract("/path/to/nonexistent/file.jpg")

    assert metadata["captured_at"] is None
    assert metadata["gps_latitude"] is None
    assert metadata["gps_longitude"] is None
    assert metadata["gps_altitude"] is None


def test_empty_method():
    """Test the _empty method directly"""
    extractor = ExifMetadataExtractor()
    empty_metadata = extractor._empty()

    assert empty_metadata == {
        "captured_at": None,
        "gps_latitude": None,
        "gps_longitude": None,
        "gps_altitude": None,
    }
