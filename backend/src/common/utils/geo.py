"""
Utility functions for geographical calculations
"""

import math
from typing import Tuple

RADIUS_EARTH_M = 6371000.0


def dms_to_decimal(dms: Tuple[float, float, float]) -> float:
    """
    Convert coordinates from degrees, minutes, seconds format to decimal degrees

    Args:
        dms: Tuple containing (degrees, minutes, seconds)

    Returns:
        Coordinate in decimal degrees
    """
    degrees, minutes, seconds = dms
    return degrees + (minutes / 60) + (seconds / 3600)


def decimal_to_dms(decimal: float) -> Tuple[float, float, float]:
    """
    Convert coordinate from decimal degrees to degrees, minutes, seconds format

    Args:
        decimal: Coordinate in decimal degrees

    Returns:
        Tuple containing (degrees, minutes, seconds)
    """
    absolute = abs(decimal)
    degrees = int(absolute)
    minutes_decimal = (absolute - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60

    if decimal < 0:
        degrees = -degrees

    return (degrees, minutes, seconds)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Args:
        lat1: Latitude of the first point
        lon1: Longitude of the first point
        lat2: Latitude of the second point
        lon2: Longitude of the second point

    Returns:
        Distance in meters
    """
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    r = RADIUS_EARTH_M

    return c * r
