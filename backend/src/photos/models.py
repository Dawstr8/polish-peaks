from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from src.peaks.models import Peak


class SummitPhoto(SQLModel, table=True):
    """Database model for a summit photo with metadata"""

    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    captured_at: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    peak_id: Optional[int] = Field(default=None, foreign_key="peak.id")
    distance_to_peak: Optional[float] = None

    peak: Optional[Peak] = Relationship()


class SummitPhotoCreate(BaseModel):
    """Request model for creating a new photo with metadata"""

    captured_at: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    peak_id: Optional[int] = None
    distance_to_peak: Optional[float] = None


class SummitPhotoRead(BaseModel):
    """Response model for reading a photo with metadata"""

    id: int
    file_name: str
    uploaded_at: datetime
    captured_at: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    peak_id: Optional[int] = None
    distance_to_peak: Optional[float] = None
    peak: Optional[Peak] = None
