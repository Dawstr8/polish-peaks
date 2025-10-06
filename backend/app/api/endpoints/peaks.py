from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.peak import Peak

router = APIRouter()


@router.get("/", response_model=list[Peak], tags=["peaks"])
def get_peaks(session: Session = Depends(get_session)):
    """
    Retrieve all peaks.
    """
    query = select(Peak)

    peaks = session.exec(query).all()
    return peaks


@router.get("/{peak_id}", response_model=Peak, tags=["peaks"])
def get_peak(peak_id: int, session: Session = Depends(get_session)):
    """
    Get a specific peak by ID.
    """
    peak = session.get(Peak, peak_id)
    if not peak:
        raise HTTPException(status_code=404, detail="Peak not found")

    return peak
