"""
Tests for the PeakService
"""

from unittest.mock import MagicMock

import pytest

from src.peaks.repository import PeakRepository
from src.peaks.service import PeakService
from tests.fixtures.peak_fixtures import peak_coords, peak_models


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
