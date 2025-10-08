from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import UploadFile

from src.common.utils.geo import dms_to_decimal
from src.peaks.service import PeakService
from src.photos.model import SummitPhoto
from src.photos.repository import PhotoRepository
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
        photo_repository: PhotoRepository,
    ):
        """
        Initialize the PhotoService

        Args:
            upload_service: Service for handling file uploads and storage
            metadata_extractor: Service for extracting metadata from image files
            peak_service: Service for finding and matching peaks
            photo_repository: Repository for database operations on photos
        """
        self._upload_service = upload_service
        self._metadata_extractor = metadata_extractor
        self._peak_service = peak_service
        self._photo_repository = photo_repository

    async def process_photo_upload(self, file: UploadFile) -> SummitPhoto:
        """
        Process a photo upload - save the file, extract metadata, find matching peaks,
        and store the photo data in the database.

        Args:
            file: The uploaded photo file

        Returns:
            SummitPhoto: The saved photo object with peak relationship loaded
        """
        path = await self._upload_service.save_file(file, content_type_prefix="image/")
        time_and_location = self._extract_photo_time_and_location(path)

        latitude, longitude, altitude, captured_at = (
            time_and_location.get("latitude"),
            time_and_location.get("longitude"),
            time_and_location.get("altitude"),
            time_and_location.get("captured_at"),
        )

        peak, distance = (
            self._peak_service.find_nearest_peak(
                latitude=latitude,
                longitude=longitude,
                max_distance_m=1000.0,
            )
            if latitude and longitude
            else (None, None)
        )

        photo = SummitPhoto(
            file_name=path.split("/")[-1],
            peak_id=(peak.id if peak else None),
            distance_to_peak=distance,
            captured_at=captured_at,
            altitude=altitude,
            latitude=latitude,
            longitude=longitude,
        )

        saved_photo = self._photo_repository.save(photo)

        return saved_photo

    def _extract_photo_time_and_location(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from the photo file.

        Args:
            file_path: Path to the photo file
        Returns:

            Dict[str, Any]: Extracted metadata
        """
        metadata = self._metadata_extractor.extract(file_path)

        captured_at, gps_latitude, gps_longitude, altitude = (
            metadata.get("captured_at"),
            metadata.get("gps_latitude"),
            metadata.get("gps_longitude"),
            metadata.get("gps_altitude"),
        )

        if isinstance(captured_at, str):
            try:
                date_parts = captured_at.split(" ")
                if len(date_parts) == 2:
                    date_str = date_parts[0].replace(":", "-")
                    captured_at = datetime.strptime(
                        f"{date_str} {date_parts[1]}", "%Y-%m-%d %H:%M:%S"
                    )
            except ValueError:
                pass

        latitude = dms_to_decimal(gps_latitude) if gps_latitude else None
        longitude = dms_to_decimal(gps_longitude) if gps_longitude else None

        return {
            "captured_at": captured_at,
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
        }

    async def get_photo_by_id(self, photo_id: int) -> Optional[SummitPhoto]:
        """
        Get a photo by its ID.

        Args:
            photo_id: ID of the photo to retrieve

        Returns:
            SummitPhoto if found, None otherwise
        """
        return self._photo_repository.get_by_id(photo_id)

    async def get_all_photos(self) -> List[SummitPhoto]:
        """
        Get all photos from the database.

        Returns:
            List[SummitPhoto]: List of all photos
        """
        return self._photo_repository.get_all()

    async def delete_photo(self, photo_id: int) -> bool:
        """
        Delete a photo by ID (both file and database record)

        Args:
            photo_id: ID of the photo to delete

        Returns:
            bool: True if deletion was successful
        """
        photo = self._photo_repository.get_by_id(photo_id)
        if not photo:
            return False

        file_deleted = await self._upload_service.delete_file(photo.file_name)

        if file_deleted:
            db_deleted = self._photo_repository.delete(photo_id)
            return db_deleted

        return False
