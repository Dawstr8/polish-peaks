from datetime import datetime, timedelta
from uuid import UUID

from sqlmodel import Session, select

from src.sessions.models import Session as UserSession


class SessionsRepository:
    """
    Repository for managing user sessions.
    """

    def __init__(self, db: Session):
        """
        Initialize the SessionsRepository.

        Args:
            db: Database session
        """
        self.db = db

    def create(self, user_id: int, expires_in_days: int) -> UserSession:
        """
        Create a new user session.

        Args:
            user_id: ID of the user to create session for
            expires_in_days: Number of days until session expiration

        Returns:
            Created session object
        """
        session = UserSession(
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days),
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_active_by_id(self, session_id: UUID) -> UserSession | None:
        """
        Get an active session by ID.

        Args:
            session_id: UUID of the session to retrieve

        Returns:
            Session if found and active, else None
        """
        statement = select(UserSession).where(
            UserSession.id == session_id,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow(),
        )

        return self.db.exec(statement).first()

    def invalidate_by_id(self, session_id: UUID) -> None:
        """
        Invalidate a session.

        Args:
            session_id: UUID of the session to invalidate
        """
        session = self.get_active_by_id(session_id)

        if session:
            session.is_active = False
            self.db.commit()
