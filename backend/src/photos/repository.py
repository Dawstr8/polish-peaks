from typing import List, Optional

from sqlmodel import delete, select

from src.database.core import DbSession
from src.photos.model import SummitPhoto


class PhotoRepository:
    """
    Repository for SummitPhoto data access operations.
    """

    def __init__(self, db: DbSession):
        """
        Initialize the PhotoRepository.

        Args:
            db: Database session
        """
        self.db: DbSession = db

    def save(self, photo: SummitPhoto) -> SummitPhoto:
        """
        Save a photo to the database.

        Args:
            photo: The SummitPhoto to save

        Returns:
            The saved SummitPhoto with database ID assigned
        """
        self.db.add(photo)
        self.db.commit()
        self.db.refresh(photo)
        return photo

    def get_by_id(self, photo_id: int) -> Optional[SummitPhoto]:
        """
        Get a specific photo by ID.

        Args:
            photo_id: ID of the photo to retrieve

        Returns:
            SummitPhoto if found, None otherwise
        """
        return self.db.get(SummitPhoto, photo_id)

    def delete(self, photo_id: int) -> bool:
        """
        Delete a photo by ID.

        Args:
            photo_id: ID of the photo to delete

        Returns:
            True if photo was deleted, False if not found
        """
        photo = self.get_by_id(photo_id)
        if not photo:
            return False

        self.db.delete(photo)
        self.db.commit()
        return True
