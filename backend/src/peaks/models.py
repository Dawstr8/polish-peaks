from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Peak(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    elevation: int
    latitude: float
    longitude: float
    range: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PeakWithDistance(BaseModel):
    """Response model for peak with distance information"""

    peak: Peak
    distance: float
