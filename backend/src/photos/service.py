from typing import Any, Dict, Optional

from fastapi import UploadFile

from src.common.utils.geo import dms_to_decimal
from src.peaks.service import PeakService
from src.photos.services.metadata_extractor import MetadataExtractorInterface
from src.uploads.service import UploadService


class PhotoService:
    """
    Service for handling photo operations including upload, metadata extraction,
    peak matching, and deletion.
    """

    def __init__(
        self,
        upload_service: UploadService,
        metadata_extractor: MetadataExtractorInterface,
        peak_service: PeakService,
    ):
        """
        Initialize the PhotoService

        Args:
            upload_service: Service for handling file uploads and storage
            metadata_extractor: Service for extracting metadata from image files
            peak_service: Service for finding and matching peaks
        """
        self._upload_service = upload_service
        self._metadata_extractor = metadata_extractor
        self._peak_service = peak_service

    async def process_photo_upload(self, file: UploadFile) -> Dict[str, Any]:
        """
        Process a photo upload - save the file, extract metadata, and find matching peaks

        Args:
            file: The uploaded photo file

        Returns:
            Dict containing the path/URL of the uploaded photo, metadata, and matched peak information
        """
        path = await self._upload_service.save_file(file, content_type_prefix="image/")
        metadata = self._metadata_extractor.extract(path)
        matched_peak_info = self._find_matching_peak(metadata)

        return {
            "success": True,
            "path": path,
            "metadata": metadata,
            "matched_peak": matched_peak_info,
        }

    def _find_matching_peak(self, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find a matching peak based on the photo's GPS coordinates

        Args:
            metadata: The photo metadata including GPS coordinates

        Returns:
            Dict with peak information or None if no matching peak is found
        """
        if not metadata.get("gps_latitude") or not metadata.get("gps_longitude"):
            return None

        match_result = self._peak_service.find_nearest_peak(
            latitude=dms_to_decimal(metadata["gps_latitude"]),
            longitude=dms_to_decimal(metadata["gps_longitude"]),
            max_distance_m=5000.0,
        )

        if not match_result:
            return None

        peak, distance = match_result
        return {
            "id": peak.id,
            "name": peak.name,
            "elevation": peak.elevation,
            "range": peak.range,
            "distance_m": round(distance, 2),
        }

    async def delete_photo(self, filename: str) -> bool:
        """
        Delete a photo file

        Args:
            filename: Name of the file to delete

        Returns:
            bool: True if deletion was successful
        """
        return await self._upload_service.delete_file(filename)
