"""
Tests for the PeakService
"""

from unittest.mock import MagicMock

import pytest

from src.peaks.model import Peak
from src.peaks.repository import PeakRepository
from src.peaks.service import PeakService


def test_find_nearest_peak():
    """Test finding the nearest peak"""
    rysy = Peak(
        id=1,
        name="Rysy",
        elevation=2499,
        latitude=49.1795,
        longitude=20.0881,
        range="Tatry",
    )

    giewont = Peak(
        id=2,
        name="Giewont",
        elevation=1894,
        latitude=49.2522,
        longitude=19.9344,
        range="Tatry",
    )

    mock_repo = MagicMock(spec=PeakRepository)
    mock_repo.get_all.return_value = [rysy, giewont]

    service = PeakService(mock_repo)

    near_rysy = (49.1794, 20.0880)
    peak, distance = service.find_nearest_peak(
        latitude=near_rysy[0], longitude=near_rysy[1], max_distance_m=5000.0
    )

    assert peak.id == 1
    assert peak.name == "Rysy"
    assert distance < 100

    mock_repo.get_all.assert_called_once()


def test_find_nearest_peak_no_peaks():
    """Test finding the nearest peak when no peaks exist"""
    mock_repo = MagicMock(spec=PeakRepository)
    mock_repo.get_all.return_value = []

    service = PeakService(mock_repo)

    near_rysy = (49.1794, 20.0880)
    peak, distance = service.find_nearest_peak(
        latitude=near_rysy[0], longitude=near_rysy[1], max_distance_m=5000.0
    )

    assert peak is None
    assert distance is None

    mock_repo.get_all.assert_called_once()


def test_find_nearest_peak_none_in_range():
    """Test finding the nearest peak when none are within range"""
    babia_gora = Peak(
        id=3,
        name="Babia Góra",
        elevation=1725,
        latitude=49.5731,
        longitude=19.5292,
        range="Beskidy",
    )

    mock_repo = MagicMock(spec=PeakRepository)
    mock_repo.get_all.return_value = [babia_gora]

    service = PeakService(mock_repo)

    warsaw = (52.2297, 21.0122)
    peak, distance = service.find_nearest_peak(
        latitude=warsaw[0], longitude=warsaw[1], max_distance_m=5000.0
    )

    assert peak is None
    assert distance is None

    mock_repo.get_all.assert_called_once()
