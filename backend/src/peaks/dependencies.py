"""Dependency injection functions and annotations for the peaks module."""

from typing import Annotated

from fastapi import Depends

from src.database.core import DbSession
from src.peaks.repository import PeakRepository
from src.peaks.service import PeakService


def get_repository(db: DbSession) -> PeakRepository:
    """Provides a PeakRepository."""
    return PeakRepository(db)


def get_service(repository: PeakRepository = Depends(get_repository)):
    """Provides a PeakService with all required dependencies."""
    return PeakService(repository)


PeakServiceDep = Annotated[PeakService, Depends(get_service)]
