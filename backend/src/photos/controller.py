from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.photos.dependencies import PhotoServiceDep
from src.photos.model import SummitPhoto

router = APIRouter(prefix="/api/photos", tags=["photos"])


@router.get("/", response_model=List[SummitPhoto], tags=["photos"])
async def get_all_photos(
    photo_service: PhotoServiceDep,
):
    """
    Get all uploaded photos

    Returns:
        List[SummitPhoto]: List of all uploaded photos
    """
    try:
        return await photo_service.get_all_photos()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve photos: {str(e)}"
        )


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


@router.get("/{photo_id}", response_model=SummitPhoto, tags=["photos"])
async def get_photo_by_id(
    photo_id: int,
    photo_service: PhotoServiceDep,
):
    """
    Get a specific photo by ID

    Args:
        photo_id: ID of the photo to retrieve

    Returns:
        SummitPhoto: The requested photo
    """
    photo = await photo_service.get_photo_by_id(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    return photo


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
