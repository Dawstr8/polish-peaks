from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Session(SQLModel, table=True):
    """Database model for user sessions"""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    is_active: bool = Field(default=True)
