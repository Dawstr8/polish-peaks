"""
Fixtures for peak-related tests
"""

import pytest

from src.common.utils.geo import decimal_to_dms
from src.peaks.model import Peak


@pytest.fixture
def peak_coords():
    """Return a dictionary of peak coordinates as (latitude, longitude) tuples"""
    return {
        "near_rysy": (49.1794, 20.0880),
        "near_sniezka": (50.7360, 15.7401),
        "warsaw": (52.2297, 21.0122),
    }


@pytest.fixture
def peak_coords_dms():
    """Return a dictionary of peak coordinates in DMS format as ((lat_d, lat_m, lat_s), (lon_d, lon_m, lon_s)) tuples"""
    return {
        "near_rysy": (decimal_to_dms(49.1794), decimal_to_dms(20.0880)),
        "near_sniezka": (decimal_to_dms(50.7360), decimal_to_dms(15.7401)),
        "warsaw": (decimal_to_dms(52.2297), decimal_to_dms(21.0122)),
    }


@pytest.fixture
def peak_models():
    """Return a dictionary of peak models"""
    return {
        "rysy": Peak(
            id=1,
            name="Rysy",
            elevation=2499,
            latitude=49.1795,
            longitude=20.0881,
            range="Tatry",
        ),
        "giewont": Peak(
            id=2,
            name="Giewont",
            elevation=1894,
            latitude=49.2522,
            longitude=19.9344,
            range="Tatry",
        ),
        "babia_gora": Peak(
            id=3,
            name="Babia Góra",
            elevation=1725,
            latitude=49.5731,
            longitude=19.5292,
            range="Beskidy",
        ),
    }
