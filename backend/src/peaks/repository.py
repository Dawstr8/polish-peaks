from typing import List, Optional

from sqlmodel import select

from src.database.core import DbSession
from src.peaks.model import Peak


class PeakRepository:
    """
    Repository for Peak data access operations.
    """

    def __init__(self, db: DbSession):
        """
        Initialize the PeakRepository.

        Args:
            db: Database session
        """
        self.db: DbSession = db

    def get_all(self) -> List[Peak]:
        """
        Retrieve all peaks.

        Returns:
            List of all peaks
        """
        query = select(Peak)
        return self.db.exec(query).all()

    def get_by_id(self, peak_id: int) -> Optional[Peak]:
        """
        Get a specific peak by ID.

        Args:
            peak_id: ID of the peak to retrieve

        Returns:
            Peak if found, None otherwise
        """
        return self.db.get(Peak, peak_id)
