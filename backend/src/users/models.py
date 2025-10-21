from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Database model for a user"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(BaseModel):
    """Request model for creating a new user"""

    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Response model for user data without sensitive information"""

    email: str
    created_at: datetime
