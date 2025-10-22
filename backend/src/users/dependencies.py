"""Dependency injection functions and annotations for the users module."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database.core import db_dep
from src.tokens.service import TokensService
from src.users.models import User
from src.users.repository import UsersRepository
from src.users.service import UsersService


def get_tokens_service():
    """Provides a TokensService instance."""
    return TokensService()


def get_repository(db: db_dep) -> UsersRepository:
    """Provides a UsersRepository."""
    return UsersRepository(db)


def get_service(
    repository: UsersRepository = Depends(get_repository),
    tokens_service: TokensService = Depends(get_tokens_service),
) -> UsersService:
    """Provides a UsersService with all required dependencies."""
    return UsersService(repository, tokens_service)


users_service_dep = Annotated[UsersService, Depends(get_service)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")


async def get_current_user(
    users_service: users_service_dep,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """
    Provides the current authenticated user.
    """
    try:
        return users_service.get_current_user_from_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


current_user_dep = Annotated[User, Depends(get_current_user)]
oauth2_password_request_form_dep = Annotated[OAuth2PasswordRequestForm, Depends()]
