import uuid
from datetime import datetime

from fastapi import UploadFile

from src.uploads.services.storage import StorageInterface


class UploadService:
    def __init__(self, storage: StorageInterface):
        self._storage = storage

    async def save_file(self, file: UploadFile, content_type_prefix: str = None) -> str:
        """
        Save an uploaded file using the configured storage provider

        Args:
            file: The uploaded file
            content_type_prefix: Optional content type validation prefix (e.g., "image/")

        Returns:
            str: The path/URL where the file was saved
        """
        if content_type_prefix and not file.content_type.startswith(
            content_type_prefix
        ):
            raise ValueError(f"File must be of type {content_type_prefix}")

        ext = file.filename.split(".")[-1].lower()
        filename = f"{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"

        return await self._storage.save_file(file, filename)

    async def delete_file(self, filename: str) -> bool:
        """
        Delete a file using the configured storage provider

        Args:
            filename: Name of the file to delete

        Returns:
            bool: True if deletion was successful
        """
        return await self._storage.delete_file(filename)
