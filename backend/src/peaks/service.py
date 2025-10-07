"""
Service for matching geographical coordinates to peaks
"""

from typing import Optional, Tuple

from src.common.utils.geo import haversine_distance
from src.peaks.model import Peak
from src.peaks.repository import PeakRepository


class PeakService:
    """
    Service for matching geographical coordinates to peaks
    based on haversine distance calculation.
    """

    def __init__(self, peak_repository: PeakRepository):
        """
        Initialize the PeakService

        Args:
            peak_repository: Repository for accessing peak data
        """
        self.peak_repository = peak_repository

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
        peaks = self.peak_repository.get_all()

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
