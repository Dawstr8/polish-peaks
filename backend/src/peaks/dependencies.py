"""Dependency injection functions and annotations for the peaks module."""

from typing import Annotated

from fastapi import Depends

from src.database.core import db_dep
from src.peaks.repository import PeaksRepository
from src.peaks.service import PeaksService


def get_repository(db: db_dep) -> PeaksRepository:
    """Provides a PeaksRepository."""
    return PeaksRepository(db)


def get_service(repository: PeaksRepository = Depends(get_repository)):
    """Provides a PeaksService with all required dependencies."""
    return PeaksService(repository)


peaks_service_dep = Annotated[PeaksService, Depends(get_service)]
