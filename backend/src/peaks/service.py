"""
Service for matching geographical coordinates to peaks
"""

from typing import List, Optional, Tuple, Union

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

    def get_all(self) -> List[Peak]:
        """
        Retrieve all peaks.

        Returns:
            List of all peaks
        """
        return self.peak_repository.get_all()

    def get_by_id(self, peak_id: int) -> Optional[Peak]:
        """
        Get a specific peak by ID.

        Args:
            peak_id: ID of the peak to retrieve

        Returns:
            Peak if found, None otherwise
        """
        return self.peak_repository.get_by_id(peak_id)

    def find_nearest_peak(
        self, latitude: float, longitude: float, max_distance_m: float = 5000.0
    ) -> Union[Tuple[Peak, float], Tuple[None, None]]:
        """
        Find the nearest peak to the given coordinates.

        Args:
            latitude: Latitude of the point
            longitude: Longitude of the point
            max_distance_m: Maximum distance in meters to search for peaks

        Returns:
            Union[Tuple[Peak, float], Tuple[None, None]]: The nearest peak and its distance in meters,
            or Tuple[None, None] if no peak is within the max distance
        """
        peaks = self.peak_repository.get_all()

        if not peaks:
            return self._empty()

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
            return self._empty()

        return min(nearby_peaks, key=lambda x: x[1])

    def _empty(self) -> Tuple[None, None]:
        """Return an empty result tuple when no peaks are found.

        Returns:
            Tuple[None, None]: A tuple with two None values
        """
        return (None, None)
