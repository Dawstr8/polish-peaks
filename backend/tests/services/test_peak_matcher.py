"""
Tests for the PeakMatcher service
"""

import pytest

from src.common.utils.geo import haversine_distance
from src.peaks.model import Peak
from src.peaks.services.peak_matcher import PeakMatcher


def test_haversine_distance():
    """Test the haversine distance calculation"""
    # Mount Everest coordinates
    lat1, lon1 = 27.9881, 86.9250

    # K2 coordinates
    lat2, lon2 = 35.8825, 76.5133

    # Distance between Everest and K2 should be around 1300000 meters (1300 km)
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    assert 1250000 < distance < 1350000


def test_find_nearest_peak(test_db):
    """Test finding the nearest peak"""
    rysy = Peak(
        name="Rysy", elevation=2499, latitude=49.1795, longitude=20.0881, range="Tatry"
    )
    test_db.add(rysy)

    sniezka = Peak(
        name="Śnieżka",
        elevation=1602,
        latitude=50.7361,
        longitude=15.7400,
        range="Karkonosze",
    )
    test_db.add(sniezka)

    test_db.commit()
    test_db.refresh(rysy)
    test_db.refresh(sniezka)

    peak_matcher = PeakMatcher(test_db)

    # Test point very close to Rysy
    near_rysy = (49.1794, 20.0880)

    result = peak_matcher.find_nearest_peak(
        latitude=near_rysy[0], longitude=near_rysy[1], max_distance_m=5000.0
    )

    assert result is not None
    peak, distance = result
    assert peak.name == "Rysy"
    assert distance < 20


def test_find_nearest_peak_too_far(test_db):
    """Test finding a peak that is too far"""
    rysy = Peak(
        name="Rysy", elevation=2499, latitude=49.1795, longitude=20.0881, range="Tatry"
    )
    test_db.add(rysy)
    test_db.commit()

    peak_matcher = PeakMatcher(test_db)

    # Test point far from Rysy (Warsaw coordinates)
    warsaw = (52.2297, 21.0122)

    result = peak_matcher.find_nearest_peak(
        latitude=warsaw[0],
        longitude=warsaw[1],
        max_distance_m=5000.0,
    )

    assert result is None
