from fastapi import APIRouter, Depends, HTTPException

from src.database.core import DbSession
from src.peaks.model import Peak
from src.peaks.repository import PeakRepository

router = APIRouter(
    prefix="/api/peaks",
    tags=["peaks"],
)


def get_repository(db: DbSession) -> PeakRepository:
    """
    Dependency to get an instance of the PeakRepository.

    Args:
        db: Database session

    Returns:
        PeakRepository instance
    """
    return PeakRepository(db)


@router.get("/", response_model=list[Peak], tags=["peaks"])
def get_peaks(repository: PeakRepository = Depends(get_repository)):
    """
    Retrieve all peaks.
    """
    return repository.get_all()


@router.get("/{peak_id}", response_model=Peak, tags=["peaks"])
def get_peak(peak_id: int, repository: PeakRepository = Depends(get_repository)):
    """
    Get a specific peak by ID.
    """
    peak = repository.get_by_id(peak_id)
    if not peak:
        raise HTTPException(status_code=404, detail="Peak not found")

    return peak
