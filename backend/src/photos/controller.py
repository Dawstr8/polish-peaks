from fastapi import APIRouter, File, HTTPException, UploadFile

from src.photos.dependencies import PhotoServiceDep

router = APIRouter(prefix="/api/photos", tags=["photos"])


@router.post("/upload")
async def upload_photo(
    photo_service: PhotoServiceDep,
    file: UploadFile = File(...),
):
    """
    Upload a photo file and find matching peaks

    Returns:
        dict: Contains the path/URL of the uploaded photo, metadata, and matched peak information
    """
    try:
        return await photo_service.process_photo_upload(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload photo: {str(e)}")


@router.delete("/{filename}")
async def delete_photo(
    filename: str,
    photo_service: PhotoServiceDep,
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
