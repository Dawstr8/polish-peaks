"""Dependency injection functions and annotations for the auth module."""

from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, status

from src.auth.password_service import PasswordService
from src.auth.service import AuthService
from src.database.core import db_dep
from src.sessions.repository import SessionsRepository
from src.users.models import User
from src.users.repository import UsersRepository


def get_users_repository(db: db_dep) -> UsersRepository:
    """Provides a UsersRepository."""
    return UsersRepository(db)


def get_sessions_repository(db: db_dep) -> SessionsRepository:
    """Provides a SessionsRepository."""
    return SessionsRepository(db)


def get_password_service():
    """Provides a PasswordService instance."""
    return PasswordService()


def get_service(
    users_repository: UsersRepository = Depends(get_users_repository),
    sessions_repository: SessionsRepository = Depends(get_sessions_repository),
    password_service: PasswordService = Depends(get_password_service),
) -> AuthService:
    """Provides a AuthService with all required dependencies."""
    return AuthService(users_repository, sessions_repository, password_service)


auth_service_dep = Annotated[AuthService, Depends(get_service)]


async def get_current_user(
    auth_service: auth_service_dep,
    session_id: UUID = Cookie(None, alias="session_id"),
) -> User:
    """
    Provides the current authenticated user from session cookie.
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        return auth_service.get_current_user(session_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )


current_user_dep = Annotated[User, Depends(get_current_user)]
