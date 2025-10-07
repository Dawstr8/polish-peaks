"""
Tests for the geo.py utility functions
"""

import pytest

from src.common.utils.geo import dms_to_decimal, haversine_distance


def test_dms_to_decimal():
    """Test degrees, minutes, seconds to decimal conversion"""
    assert dms_to_decimal((49.0, 12.0, 4.84)) == pytest.approx(49.201344)
    assert dms_to_decimal((0.0, 30.0, 0.0)) == pytest.approx(0.5)
    assert dms_to_decimal((50.0, 0.0, 0.0)) == 50.0


def test_haversine_distance():
    """Test the haversine distance calculation"""
    # Mount Everest coordinates
    lat1, lon1 = 27.9881, 86.9250

    # K2 coordinates
    lat2, lon2 = 35.8825, 76.5133

    # Distance between Everest and K2 should be around 1300 km (1,300,000 m)
    distance = haversine_distance(lat1, lon1, lat2, lon2)

    assert 1250000 < distance < 1350000
