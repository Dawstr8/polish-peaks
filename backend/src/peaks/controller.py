from fastapi import APIRouter, HTTPException

from src.peaks.dependencies import PeakServiceDep
from src.peaks.model import Peak

router = APIRouter(
    prefix="/api/peaks",
    tags=["peaks"],
)


@router.get("/", response_model=list[Peak], tags=["peaks"])
def get_peaks(service: PeakServiceDep):
    """
    Retrieve all peaks.
    """
    return service.get_all()


@router.get("/{peak_id}", response_model=Peak, tags=["peaks"])
def get_peak(peak_id: int, service: PeakServiceDep):
    """
    Get a specific peak by ID.
    """
    peak = service.get_by_id(peak_id)
    if not peak:
        raise HTTPException(status_code=404, detail="Peak not found")

    return peak
