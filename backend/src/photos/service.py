from typing import List, Optional

from fastapi import UploadFile

from src.peaks.service import PeakService
from src.photos.model import SummitPhoto, SummitPhotoCreate
from src.photos.repository import PhotoRepository
from src.uploads.service import UploadService


class PhotoService:
    """
    Service for handling photo operations.
    """

    def __init__(
        self,
        upload_service: UploadService,
        peak_service: PeakService,
        photo_repository: PhotoRepository,
    ):
        """
        Initialize the PhotoService

        Args:
            upload_service: Service for handling file uploads and storage
            peak_service: Service for finding and matching peaks
            photo_repository: Repository for database operations on photos
        """
        self._upload_service = upload_service
        self._peak_service = peak_service
        self._photo_repository = photo_repository

    async def upload_photo(
        self, file: UploadFile, summit_photo_create: SummitPhotoCreate
    ) -> SummitPhoto:
        """
        Upload a photo file and store it in the database with the provided metadata.

        Args:
            file: The uploaded photo file
            summit_photo_create: Metadata for the photo (captured_at, latitude, longitude, altitude, peak_id, distance_to_peak)

        Returns:
            SummitPhoto: The saved photo object
        """
        path = await self._upload_service.save_file(file, content_type_prefix="image/")

        photo = SummitPhoto(
            file_name=path.split("/")[-1],
            **summit_photo_create.model_dump(),
        )

        saved_photo = self._photo_repository.save(photo)

        return saved_photo

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
