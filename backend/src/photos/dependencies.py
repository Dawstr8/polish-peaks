"""
Dependency injection functions and annotations for the photos module.
Uses Python's Annotated type to create cleaner FastAPI dependency injections.
"""

from typing import Annotated

from fastapi import Depends

from src.database.core import DbSession
from src.peaks.repository import PeakRepository
from src.peaks.service import PeakService
from src.photos.service import PhotoService
from src.photos.services.exif_metadata_extractor import ExifMetadataExtractor
from src.photos.services.metadata_extractor import MetadataExtractorInterface
from src.uploads.service import UploadService
from src.uploads.services.local_storage import LocalFileStorage


def get_upload_service() -> UploadService:
    """Provides a configured UploadService with LocalFileStorage."""
    storage = LocalFileStorage()
    return UploadService(storage)


def get_metadata_extractor() -> MetadataExtractorInterface:
    """Provides a metadata extractor implementation."""
    return ExifMetadataExtractor()


def get_peak_service(db: DbSession) -> PeakService:
    """Provides a PeakService with repository."""
    repository = PeakRepository(db)
    return PeakService(repository)


def get_photo_service(
    upload_service: UploadService = Depends(get_upload_service),
    metadata_extractor: MetadataExtractorInterface = Depends(get_metadata_extractor),
    peak_service: PeakService = Depends(get_peak_service),
) -> PhotoService:
    """Provides a PhotoService with all required dependencies."""
    return PhotoService(upload_service, metadata_extractor, peak_service)


PhotoServiceDep = Annotated[PhotoService, Depends(get_photo_service)]
