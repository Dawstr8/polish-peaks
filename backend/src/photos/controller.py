from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from src.common.utils.geo import dms_to_decimal
from src.database.core import DbSession
from src.peaks.repository import PeakRepository
from src.peaks.service import PeakService
from src.photos.services.exif_metadata_extractor import ExifMetadataExtractor
from src.photos.services.metadata_extractor import MetadataExtractorInterface
from src.uploads.service import UploadService
from src.uploads.services.local_storage import LocalFileStorage

router = APIRouter(prefix="/api/photos", tags=["photos"])


def get_upload_service():
    storage = LocalFileStorage()
    return UploadService(storage)


def get_metadata_extractor() -> MetadataExtractorInterface:
    return ExifMetadataExtractor()


def get_peak_service(db: DbSession) -> PeakService:
    """
    Dependency to get an instance of the PeakService.

    Args:
        db: Database session

    Returns:
        PeakService instance
    """
    repository = PeakRepository(db)
    return PeakService(repository)


@router.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    upload_service: UploadService = Depends(get_upload_service),
    metadata_extractor: MetadataExtractorInterface = Depends(get_metadata_extractor),
    peak_service: PeakService = Depends(get_peak_service),
):
    """
    Upload a photo file and find matching peaks

    Returns:
        dict: Contains the path/URL of the uploaded photo, metadata, and matched peak information
    """
    try:
        path = await upload_service.save_file(file, content_type_prefix="image/")
        metadata = metadata_extractor.extract(path)

        matched_peak_info = None
        if metadata.get("gps_latitude") and metadata.get("gps_longitude"):
            match_result = peak_service.find_nearest_peak(
                latitude=dms_to_decimal(metadata["gps_latitude"]),
                longitude=dms_to_decimal(metadata["gps_longitude"]),
                max_distance_m=5000.0,
            )

            if match_result:
                peak, distance = match_result
                matched_peak_info = {
                    "id": peak.id,
                    "name": peak.name,
                    "elevation": peak.elevation,
                    "range": peak.range,
                    "distance_m": round(distance, 2),
                }

        return {
            "success": True,
            "path": path,
            "metadata": metadata,
            "matched_peak": matched_peak_info,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload photo: {str(e)}")


@router.delete("/{filename}")
async def delete_photo(
    filename: str, upload_service: UploadService = Depends(get_upload_service)
):
    """
    Delete an uploaded photo

    Args:
        filename: Name of the file to delete

    Returns:
        dict: Success status of the operation
    """
    success = await upload_service.delete_file(filename)

    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")

    return {"success": True}
