"""Dependency injection functions and annotations for the peaks module."""

from typing import Annotated

from fastapi import Depends

from src.database.core import db_dep
from src.peaks.repository import PeakRepository
from src.peaks.service import PeakService


def get_repository(db: db_dep) -> PeakRepository:
    """Provides a PeakRepository."""
    return PeakRepository(db)


def get_service(repository: PeakRepository = Depends(get_repository)):
    """Provides a PeakService with all required dependencies."""
    return PeakService(repository)


peak_service_dep = Annotated[PeakService, Depends(get_service)]
