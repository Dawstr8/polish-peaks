from src.database.core import DbSession
from src.users.models import User


class UsersRepository:
    """
    Repository for User data access operations.
    """

    def __init__(self, db: DbSession):
        """
        Initialize the UsersRepository.

        Args:
            db: Database session
        """
        self.db: DbSession = db

    def save(self, user: User) -> User:
        """
        Save a user to the database. Raises ValueError if email already exists.

        Args:
            user: The User to save

        Returns:
            The saved User object with database ID assigned
        """
        from sqlalchemy.exc import IntegrityError

        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            if "unique" in str(e).lower() and "email" in str(e).lower():
                raise ValueError("Email is already in use.")

            raise

        self.db.refresh(user)
        return user
