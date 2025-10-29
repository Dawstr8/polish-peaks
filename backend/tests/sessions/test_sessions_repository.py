import pytest
from sqlmodel import Session

from src.sessions.repository import SessionsRepository


@pytest.fixture
def test_sessions_repository(test_db: Session) -> SessionsRepository:
    """Create a SessionsRepository instance for testing."""
    return SessionsRepository(test_db)


def test_create_session(test_sessions_repository: SessionsRepository):
    """Test creating a new session"""
    user_id = 1
    expires_in_days = 7

    session = test_sessions_repository.create(user_id, expires_in_days)

    assert session.id is not None
    assert session.user_id == user_id
    assert session.is_active


def test_get_active_by_id_valid(test_sessions_repository: SessionsRepository):
    """Test retrieving valid active session by ID"""
    user_id = 1
    session = test_sessions_repository.create(user_id, expires_in_days=7)

    retrieved_session = test_sessions_repository.get_active_by_id(session.id)

    assert retrieved_session is not None
    assert retrieved_session.id == session.id
    assert retrieved_session.user_id == user_id
    assert retrieved_session.is_active


def test_get_active_by_id_expired(test_sessions_repository: SessionsRepository):
    """Test retrieving expired session by ID returns None"""
    user_id = 1
    session = test_sessions_repository.create(user_id, expires_in_days=0)

    retrieved_session = test_sessions_repository.get_active_by_id(session.id)

    assert retrieved_session is None


def test_get_active_by_id_invalidated(test_sessions_repository: SessionsRepository):
    """Test retrieving invalidated session by ID returns None"""
    user_id = 1
    session = test_sessions_repository.create(user_id, expires_in_days=7)
    test_sessions_repository.invalidate_by_id(session.id)

    retrieved_session = test_sessions_repository.get_active_by_id(session.id)

    assert retrieved_session is None


def test_invalidate_by_id(test_sessions_repository: SessionsRepository):
    """Test invalidating a session"""
    user_id = 1
    session = test_sessions_repository.create(user_id, expires_in_days=7)

    test_sessions_repository.invalidate_by_id(session.id)

    inactive_session = test_sessions_repository.get_active_by_id(session.id)
    assert inactive_session is None
