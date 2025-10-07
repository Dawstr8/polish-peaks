"""
Tests for the PhotoRepository
"""

from datetime import datetime

import pytest

from src.photos.model import SummitPhoto
from src.photos.repository import PhotoRepository


@pytest.fixture()
def test_photo_repository(test_db):
    """Create a PhotoRepository instance for testing"""
    return PhotoRepository(test_db)


@pytest.fixture()
def test_photos(test_db, test_peaks):
    """Create test summit photos and save to database"""
    near_rysy = (49.1794, 20.0880)
    near_sniezka = (50.7360, 15.7401)

    photos = [
        SummitPhoto(
            file_name="test1.jpg",
            uploaded_at=datetime(2025, 10, 1, 12, 0),
            captured_at=datetime(2025, 9, 30, 10, 0),
            latitude=near_rysy[0],
            longitude=near_rysy[1],
            altitude=2495,
            peak_id=test_peaks[0].id,
            distance_to_peak=10.5,
        ),
        SummitPhoto(
            file_name="test2.jpg",
            uploaded_at=datetime(2025, 10, 2, 14, 0),
            captured_at=datetime(2025, 10, 1, 11, 0),
            latitude=near_sniezka[0],
            longitude=near_sniezka[1],
            altitude=1600,
            peak_id=test_peaks[1].id,
            distance_to_peak=5.2,
        ),
    ]

    for photo in photos:
        test_db.add(photo)

    test_db.commit()

    for photo in photos:
        test_db.refresh(photo)

    return photos


def test_save(test_photo_repository):
    """Test saving a new summit photo"""
    new_photo = SummitPhoto(
        file_name="new_photo.jpg",
        captured_at=datetime(2025, 10, 5, 9, 0),
        latitude=49.5730,
        longitude=19.5295,
        altitude=1720,
        distance_to_peak=3.8,
    )

    saved_photo = test_photo_repository.save(new_photo)

    assert saved_photo.id is not None
    assert saved_photo.file_name == "new_photo.jpg"
    assert saved_photo.captured_at == datetime(2025, 10, 5, 9, 0)
    assert saved_photo.latitude == 49.5730
    assert saved_photo.longitude == 19.5295
    assert saved_photo.altitude == 1720
    assert saved_photo.distance_to_peak == 3.8


def test_get_by_id(test_photo_repository, test_photos):
    """Test retrieving a summit photo by ID"""
    photo_id = test_photos[0].id

    photo = test_photo_repository.get_by_id(photo_id)

    assert photo is not None
    assert photo.file_name == "test1.jpg"
    assert photo.peak_id == test_photos[0].peak_id
    assert photo.distance_to_peak == 10.5


def test_get_by_id_non_existent(test_photo_repository):
    """Test retrieving a non-existent summit photo by ID"""
    non_existent_photo = test_photo_repository.get_by_id(999999)

    assert non_existent_photo is None


def test_delete(test_photo_repository, test_photos):
    """Test deleting a summit photo"""
    photo_id = test_photos[0].id
    photo = test_photo_repository.get_by_id(photo_id)
    assert photo is not None

    result = test_photo_repository.delete(photo_id)
    assert result is True

    photo = test_photo_repository.get_by_id(photo_id)
    assert photo is None


def test_delete_non_existent(test_photo_repository):
    """Test deleting a non-existent summit photo"""
    result = test_photo_repository.delete(999999)
    assert result is False
