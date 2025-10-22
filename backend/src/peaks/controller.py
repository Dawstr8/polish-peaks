from fastapi import APIRouter, HTTPException

from src.peaks.dependencies import peaks_service_dep
from src.peaks.models import Peak, PeakWithDistance

router = APIRouter(
    prefix="/api/peaks",
    tags=["peaks"],
)


@router.get("/", response_model=list[Peak], tags=["peaks"])
def get_peaks(service: peaks_service_dep):
    """
    Retrieve all peaks.
    """
    return service.get_all()


@router.get("/find", response_model=list[PeakWithDistance], tags=["peaks"])
def find_nearest_peaks(
    service: peaks_service_dep,
    latitude: float,
    longitude: float,
    max_distance: float | None = None,
    limit: int = 5,
):
    """
    Find the nearest peaks to a given latitude and longitude.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        max_distance: Maximum distance in meters (optional)
        limit: Maximum number of peaks to return (default: 5)

    Returns:
        List of nearest peaks with distances in meters
    """
    return service.find_nearest_peaks(
        latitude=latitude, longitude=longitude, max_distance=max_distance, limit=limit
    )


@router.get("/{peak_id}", response_model=Peak, tags=["peaks"])
def get_peak(peak_id: int, service: peaks_service_dep):
    """
    Get a specific peak by ID.
    """
    peak = service.get_by_id(peak_id)
    if not peak:
        raise HTTPException(status_code=404, detail="Peak not found")

    return peak
