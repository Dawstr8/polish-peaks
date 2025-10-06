"""
Service for matching geographical coordinates to peaks
"""

from typing import Optional, Tuple

from sqlmodel import Session, select

from app.models.peak import Peak
from app.utils.geo import haversine_distance


class PeakMatcher:
    """
    Service for matching geographical coordinates to peaks
    based on haversine distance calculation.
    """

    def __init__(self, session: Session):
        """
        Initialize the PeakMatcher service

        Args:
            session: SQLModel database session
        """
        self.session = session

    def find_nearest_peak(
        self, latitude: float, longitude: float, max_distance_m: float = 5000.0
    ) -> Optional[Tuple[Peak, float]]:
        """
        Find the nearest peak to the given coordinates.

        Args:
            latitude: Latitude of the point
            longitude: Longitude of the point
            max_distance_m: Maximum distance in meters to search for peaks

        Returns:
            A tuple containing the nearest peak and its distance in meters,
            or None if no peak is found within the maximum distance
        """
        peaks = self.session.exec(select(Peak)).all()

        if not peaks:
            return None

        peak_distances = [
            (
                peak,
                haversine_distance(latitude, longitude, peak.latitude, peak.longitude),
            )
            for peak in peaks
        ]

        nearby_peaks = [
            (peak, distance)
            for peak, distance in peak_distances
            if distance <= max_distance_m
        ]

        if not nearby_peaks:
            return None

        return min(nearby_peaks, key=lambda x: x[1])
