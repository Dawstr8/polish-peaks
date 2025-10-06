from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.interfaces.metadata_extractor import MetadataExtractorInterface
from app.services.exif_metadata_extractor import ExifMetadataExtractor
from app.services.photo_service import PhotoService
from app.services.storage.local_storage import LocalFileStorage

router = APIRouter()


def get_photo_service():
    storage = LocalFileStorage()
    return PhotoService(storage)


def get_metadata_extractor() -> MetadataExtractorInterface:
    return ExifMetadataExtractor()


@router.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    photo_service: PhotoService = Depends(get_photo_service),
    metadata_extractor: MetadataExtractorInterface = Depends(get_metadata_extractor),
):
    """
    Upload a photo file

    Returns:
        dict: Contains the path/URL of the uploaded photo
    """
    try:
        path = await photo_service.save_photo(file)
        metadata = metadata_extractor.extract(path)

        return {"success": True, "path": path, "metadata": metadata}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload photo")


@router.delete("/{filename}")
async def delete_photo(
    filename: str, photo_service: PhotoService = Depends(get_photo_service)
):
    """
    Delete an uploaded photo

    Args:
        filename: Name of the file to delete

    Returns:
        dict: Success status of the operation
    """
    success = await photo_service.delete_photo(filename)

    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")

    return {"success": True}
