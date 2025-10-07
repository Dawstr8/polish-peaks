from fastapi import APIRouter, File, HTTPException, UploadFile

from src.photos.dependencies import PhotoServiceDep
from src.photos.model import SummitPhoto

router = APIRouter(prefix="/api/photos", tags=["photos"])


@router.post("/", response_model=SummitPhoto, tags=["photos"])
async def upload_photo(
    photo_service: PhotoServiceDep,
    file: UploadFile = File(...),
):
    """
    Upload a photo file and find matching peaks

    Returns:
        SummitPhoto: The uploaded photo object with related peak ID
    """
    try:
        return await photo_service.process_photo_upload(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload photo: {str(e)}")


@router.delete("/{photo_id}", response_model=dict, tags=["photos"])
async def delete_photo(
    photo_id: int,
    photo_service: PhotoServiceDep,
):
    """
    Delete an uploaded photo by ID

    Args:
        photo_id: ID of the photo to delete

    Returns:
        dict: Success status of the operation
    """
    success = await photo_service.delete_photo(photo_id)

    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")

    return {"success": True}
