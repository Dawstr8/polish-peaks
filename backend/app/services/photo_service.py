import uuid
from datetime import datetime

from fastapi import UploadFile

from app.core.interfaces.storage import StorageInterface


class PhotoService:
    def __init__(self, storage: StorageInterface):
        self._storage = storage

    async def save_photo(self, photo: UploadFile) -> str:
        """
        Save an uploaded photo using the configured storage provider

        Args:
            photo: The uploaded photo file

        Returns:
            str: The path/URL where the photo was saved
        """
        if not photo.content_type.startswith("image/"):
            raise ValueError("File must be a photo")

        ext = photo.filename.split(".")[-1].lower()
        filename = f"{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"

        return await self._storage.save_file(photo, filename)

    async def delete_photo(self, filename: str) -> bool:
        """
        Delete a photo using the configured storage provider

        Args:
            filename: Name of the file to delete

        Returns:
            bool: True if deletion was successful
        """
        return await self._storage.delete_file(filename)
