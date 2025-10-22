"""
Dependency injection functions and annotations for the photos module.
Uses Python's Annotated type to create cleaner FastAPI dependency injections.
"""

from typing import Annotated

from fastapi import Depends

from src.database.core import db_dep
from src.photos.repository import PhotosRepository
from src.photos.service import PhotosService
from src.uploads.service import UploadsService
from src.uploads.services.local_storage import LocalFileStorage


def get_uploads_service() -> UploadsService:
    """Provides a configured UploadsService with LocalFileStorage."""
    storage = LocalFileStorage()
    return UploadsService(storage)


def get_photos_repository(db: db_dep) -> PhotosRepository:
    """Provides a PhotosRepository."""
    return PhotosRepository(db)


def get_photos_service(
    uploads_service: UploadsService = Depends(get_uploads_service),
    photos_repository: PhotosRepository = Depends(get_photos_repository),
) -> PhotosService:
    """Provides a PhotosService with all required dependencies."""
    return PhotosService(uploads_service, photos_repository)


photos_service_dep = Annotated[PhotosService, Depends(get_photos_service)]
