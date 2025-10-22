"""Dependency injection functions and annotations for the users module."""

from typing import Annotated

from fastapi import Depends

from src.database.core import db_dep
from src.users.repository import UsersRepository
from src.users.service import UsersService


def get_repository(db: db_dep) -> UsersRepository:
    """Provides a UsersRepository."""
    return UsersRepository(db)


def get_service(
    repository: UsersRepository = Depends(get_repository),
) -> UsersService:
    """Provides a UsersService with all required dependencies."""
    return UsersService(repository)


users_service_dep = Annotated[UsersService, Depends(get_service)]
