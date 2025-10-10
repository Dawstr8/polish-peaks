"""
Tests for the PeakService
"""

from unittest.mock import MagicMock

import pytest

from src.peaks.repository import PeakRepository
from src.peaks.service import PeakService
from tests.fixtures.peak_fixtures import peak_coords, peak_models


def test_get_all(peak_models):
    """Test getting all peaks through the service"""
    rysy = peak_models["rysy"]
    giewont = peak_models["giewont"]

    mock_repo = MagicMock(spec=PeakRepository)
    mock_repo.get_all.return_value = [rysy, giewont]

    service = PeakService(mock_repo)

    peaks = service.get_all()

    assert len(peaks) == 2
    assert peaks[0].name == "Rysy"
    assert peaks[1].name == "Giewont"

    mock_repo.get_all.assert_called_once()


def test_get_by_id(peak_models):
    """Test getting a specific peak by ID through the service"""
    rysy = peak_models["rysy"]

    mock_repo = MagicMock(spec=PeakRepository)
    mock_repo.get_by_id.return_value = rysy

    service = PeakService(mock_repo)

    peak = service.get_by_id(1)

    assert peak is not None
    assert peak.id == 1
    assert peak.name == "Rysy"

    mock_repo.get_by_id.assert_called_once_with(1)


def test_get_by_id_not_found():
    """Test getting a peak by ID when it doesn't exist"""
    mock_repo = MagicMock(spec=PeakRepository)
    mock_repo.get_by_id.return_value = None

    service = PeakService(mock_repo)

    peak = service.get_by_id(999)

    assert peak is None

    mock_repo.get_by_id.assert_called_once_with(999)


def test_find_nearest_peak(peak_models, peak_coords):
    """Test finding the nearest peak"""
    rysy = peak_models["rysy"]
    giewont = peak_models["giewont"]

    mock_repo = MagicMock(spec=PeakRepository)
    mock_repo.get_all.return_value = [rysy, giewont]

    service = PeakService(mock_repo)

    peak, distance = service.find_nearest_peak(
        latitude=peak_coords["near_rysy"][0],
        longitude=peak_coords["near_rysy"][1],
        max_distance_m=5000.0,
    )

    assert peak.id == 1
    assert peak.name == "Rysy"
    assert distance < 100

    mock_repo.get_all.assert_called_once()


def test_find_nearest_peak_no_peaks(peak_coords):
    """Test finding the nearest peak when no peaks exist"""
    mock_repo = MagicMock(spec=PeakRepository)
    mock_repo.get_all.return_value = []

    service = PeakService(mock_repo)

    peak, distance = service.find_nearest_peak(
        latitude=peak_coords["near_rysy"][0],
        longitude=peak_coords["near_rysy"][1],
        max_distance_m=5000.0,
    )

    assert peak is None
    assert distance is None

    mock_repo.get_all.assert_called_once()


def test_find_nearest_peak_none_in_range(peak_models, peak_coords):
    """Test finding the nearest peak when none are within range"""
    babia_gora = peak_models["babia_gora"]

    mock_repo = MagicMock(spec=PeakRepository)
    mock_repo.get_all.return_value = [babia_gora]

    service = PeakService(mock_repo)

    peak, distance = service.find_nearest_peak(
        latitude=peak_coords["warsaw"][0],
        longitude=peak_coords["warsaw"][1],
        max_distance_m=5000.0,
    )

    assert peak is None
    assert distance is None

    mock_repo.get_all.assert_called_once()
