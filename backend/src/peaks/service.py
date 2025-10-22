"""
Service for matching geographical coordinates to peaks
"""

from typing import Any, Dict, List, Optional

from src.common.utils.geo import haversine_distance
from src.peaks.models import Peak
from src.peaks.repository import PeaksRepository


class PeaksService:
    """
    Service for matching geographical coordinates to peaks
    based on haversine distance calculation.
    """

    def __init__(self, peaks_repository: PeaksRepository):
        """
        Initialize the PeaksService

        Args:
            peaks_repository: Repository for accessing peak data
        """
        self.peaks_repository = peaks_repository

    def get_all(self) -> List[Peak]:
        """
        Retrieve all peaks.

        Returns:
            List of all peaks
        """
        return self.peaks_repository.get_all()

    def get_by_id(self, peak_id: int) -> Optional[Peak]:
        """
        Get a specific peak by ID.

        Args:
            peak_id: ID of the peak to retrieve

        Returns:
            Peak if found, None otherwise
        """
        return self.peaks_repository.get_by_id(peak_id)

    def find_nearest_peaks(
        self,
        latitude: float,
        longitude: float,
        max_distance: float | None = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Find the nearest peaks to a given latitude and longitude using Haversine distance.

        Args:
            latitude: Latitude of the point
            longitude: Longitude of the point
            limit: Maximum number of peaks to return (default: 5)

        Returns:
            List of dictionaries containing peak and its distance from the point
        """
        peaks = self.peaks_repository.get_all()

        if not peaks:
            return []

        peaks_with_distance = [
            {
                "peak": peak,
                "distance": haversine_distance(
                    latitude, longitude, peak.latitude, peak.longitude
                ),
            }
            for peak in peaks
        ]

        if max_distance is not None:
            peaks_with_distance = [
                peak for peak in peaks_with_distance if peak["distance"] <= max_distance
            ]

        peaks_by_nearest = sorted(peaks_with_distance, key=lambda x: x["distance"])

        return peaks_by_nearest[:limit]
