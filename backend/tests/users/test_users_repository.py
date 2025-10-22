import pytest
from sqlmodel import Session

from src.users.models import User
from src.users.repository import UsersRepository


@pytest.fixture()
def test_users_repository(test_db: Session) -> UsersRepository:
    """Create a UsersRepository instance for testing."""
    return UsersRepository(test_db)


def test_save_user_success(test_users_repository):
    """Test saving a new user successfully."""
    user = User(email="test@example.com", hashed_password="hash")

    saved_user = test_users_repository.save(user)

    assert saved_user.id is not None
    assert saved_user.email == "test@example.com"


def test_save_user_duplicate_email(test_users_repository):
    """Test saving a user with a duplicate email raises ValueError."""
    test_users_repository.save(User(email="test@example.com", hashed_password="hash"))
    saved_user = User(email="test@example.com", hashed_password="hash2")

    with pytest.raises(ValueError) as exc:
        test_users_repository.save(saved_user)

    assert "Email is already in use" in str(exc.value)


def test_get_by_email_existing_user(test_users_repository):
    """Test getting an existing user by email."""
    user = User(email="test@example.com", hashed_password="hash")
    saved_user = test_users_repository.save(user)

    retrieved_user = test_users_repository.get_by_email("test@example.com")

    assert retrieved_user is not None
    assert retrieved_user.id == saved_user.id
    assert retrieved_user.email == "test@example.com"


def test_get_by_email_non_existing_user(test_users_repository):
    """Test getting a non-existing user by email returns None."""
    retrieved_user = test_users_repository.get_by_email("nonexistent@example.com")

    assert retrieved_user is None
