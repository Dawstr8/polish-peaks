from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session

from app.core.interfaces.metadata_extractor import MetadataExtractorInterface
from app.database import get_session
from app.services.exif_metadata_extractor import ExifMetadataExtractor
from app.services.peak_matcher import PeakMatcher
from app.services.storage.local_storage import LocalFileStorage
from app.services.upload_service import UploadService
from app.utils.geo import dms_to_decimal

router = APIRouter()


def get_upload_service():
    storage = LocalFileStorage()
    return UploadService(storage)


def get_metadata_extractor() -> MetadataExtractorInterface:
    return ExifMetadataExtractor()


@router.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    upload_service: UploadService = Depends(get_upload_service),
    metadata_extractor: MetadataExtractorInterface = Depends(get_metadata_extractor),
    session: Session = Depends(get_session),
):
    """
    Upload a photo file and find matching peaks

    Returns:
        dict: Contains the path/URL of the uploaded photo, metadata, and matched peak information
    """
    try:
        path = await upload_service.save_photo(file)
        metadata = metadata_extractor.extract(path)

        matched_peak_info = None
        if metadata.get("gps_latitude") and metadata.get("gps_longitude"):
            peak_matcher = PeakMatcher(session)
            match_result = peak_matcher.find_nearest_peak(
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
    success = await upload_service.delete_photo(filename)

    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")

    return {"success": True}
