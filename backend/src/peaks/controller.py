from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.database.core import DbSession
from src.peaks.model import Peak

router = APIRouter(
    prefix="/api/peaks",
    tags=["peaks"],
)


@router.get("/", response_model=list[Peak], tags=["peaks"])
def get_peaks(db: DbSession):
    """
    Retrieve all peaks.
    """
    query = select(Peak)

    peaks = db.exec(query).all()
    return peaks


@router.get("/{peak_id}", response_model=Peak, tags=["peaks"])
def get_peak(peak_id: int, db: DbSession):
    """
    Get a specific peak by ID.
    """
    peak = db.get(Peak, peak_id)
    if not peak:
        raise HTTPException(status_code=404, detail="Peak not found")

    return peak
