from typing import List, Optional

from sqlmodel import Session, desc, select

from src.photos.model import SummitPhoto


class PhotoRepository:
    """
    Repository for SummitPhoto data access operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the PhotoRepository.

        Args:
            db: Database session
        """
        self.db = db

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

    def get_all(
        self, sort_by: Optional[str] = None, order: Optional[str] = None
    ) -> List[SummitPhoto]:
        """
        Get all photos from the database, optionally sorted.

        Args:
            sort_by: Field to sort by (optional)
            order: Sort order 'desc' for descending, otherwise ascending (SQL default)

        Returns:
            List of SummitPhoto objects
        """
        statement = select(SummitPhoto)

        if sort_by and hasattr(SummitPhoto, sort_by):
            column = getattr(SummitPhoto, sort_by)
            statement = (
                statement.order_by(desc(column))
                if order == "desc"
                else statement.order_by(column)
            )

        results = self.db.exec(statement).all()
        return results

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
