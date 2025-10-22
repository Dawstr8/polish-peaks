from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

from src.photos.dependencies import photo_service_dep
from src.photos.model import SummitPhotoCreate, SummitPhotoRead

router = APIRouter(prefix="/api/photos", tags=["photos"])


@router.get("/", response_model=List[SummitPhotoRead], tags=["photos"])
async def get_all_photos(
    photo_service: photo_service_dep,
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query(None, description="Sort order: 'asc' or 'desc'"),
):
    """
    Get all uploaded photos, optionally sorted by a field.

    Args:
        sort_by: Field to sort by (optional).
        order: Sort order 'desc' for descending, otherwise ascending (SQL default). Only used if sort_by is provided.

    Returns:
        List[SummitPhotoRead]: List of all uploaded photos, with peak information, sorted as specified or in default order.
    """
    try:
        return await photo_service.get_all_photos(sort_by=sort_by, order=order)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve photos: {str(e)}"
        )


@router.post("/", response_model=SummitPhotoRead, tags=["photos"])
async def upload_photo(
    photo_service: photo_service_dep,
    file: UploadFile = File(...),
    summit_photo_create: str = Form(...),
):
    """
    Upload a photo file with metadata

    Args:
        file: The photo file to upload
        summit_photo_create: Metadata for the photo (captured_at, latitude, longitude, altitude, peak_id, distance_to_peak)

    Returns:
        SummitPhotoRead: The uploaded photo object with peak information
    """
    summit_photo_create = SummitPhotoCreate.model_validate_json(summit_photo_create)

    try:
        return await photo_service.upload_photo(file, summit_photo_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload photo: {str(e)}")


@router.get("/{photo_id}", response_model=SummitPhotoRead, tags=["photos"])
async def get_photo_by_id(
    photo_id: int,
    photo_service: photo_service_dep,
):
    """
    Get a specific photo by ID

    Args:
        photo_id: ID of the photo to retrieve

    Returns:
        SummitPhotoRead: The requested photo object with peak information
    """
    photo = await photo_service.get_photo_by_id(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    return photo


@router.delete("/{photo_id}", response_model=dict, tags=["photos"])
async def delete_photo(
    photo_id: int,
    photo_service: photo_service_dep,
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
