"""Dependency injection functions and annotations for the auth module."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.password_service import PasswordService
from src.auth.service import AuthService
from src.database.core import db_dep
from src.tokens.service import TokensService
from src.users.models import User
from src.users.repository import UsersRepository


def get_users_repository(db: db_dep) -> UsersRepository:
    """Provides a UsersRepository."""
    return UsersRepository(db)


def get_tokens_service():
    """Provides a TokensService instance."""
    return TokensService()


def get_password_service():
    """Provides a PasswordService instance."""
    return PasswordService()


def get_service(
    users_repository: UsersRepository = Depends(get_users_repository),
    tokens_service: TokensService = Depends(get_tokens_service),
    password_service: PasswordService = Depends(get_password_service),
) -> AuthService:
    """Provides a AuthService with all required dependencies."""
    return AuthService(users_repository, tokens_service, password_service)


auth_service_dep = Annotated[AuthService, Depends(get_service)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    auth_service: auth_service_dep,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """
    Provides the current authenticated user.
    """
    try:
        return auth_service.get_current_user_from_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


current_user_dep = Annotated[User, Depends(get_current_user)]
oauth2_password_request_form_dep = Annotated[OAuth2PasswordRequestForm, Depends()]
