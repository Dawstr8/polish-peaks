from enum import Enum

from pydantic import BaseModel


class TokenTypes(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class Token(BaseModel):
    access_token: str
    token_type: str
