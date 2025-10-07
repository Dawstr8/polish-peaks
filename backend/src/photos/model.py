from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from src.peaks.model import Peak


class SummitPhoto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    captured_at: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    peak_id: Optional[int] = Field(default=None, foreign_key="peak.id")
    distance_to_peak: Optional[float] = None
