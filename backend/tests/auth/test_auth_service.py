from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.auth.password_service import PasswordService
from src.auth.service import AuthService
from src.sessions.repository import SessionsRepository
from src.users.models import User, UserCreate
from src.users.repository import UsersRepository


@pytest.fixture
def mock_users_repository():
    """Create a mock UsersRepository"""
    repo = MagicMock(spec=UsersRepository)

    def save_user(user):
        user.id = 1
        return user

    repo.save.side_effect = save_user
    return repo


@pytest.fixture
def mock_sessions_repository():
    """Create a mock SessionsRepository"""
    return MagicMock(spec=SessionsRepository)


@pytest.fixture
def mock_password_service():
    """Create a mock PasswordService"""
    password_service = MagicMock()
    password_service.get_hash.side_effect = lambda pwd: f"hashed_{pwd}"
    password_service.verify.side_effect = (
        lambda plain, hashed: hashed == f"hashed_{plain}"
    )
    return password_service


@pytest.fixture
def service(
    mock_users_repository: UsersRepository,
    mock_sessions_repository: SessionsRepository,
    mock_password_service: PasswordService,
) -> AuthService:
    """Create an AuthService with mocked dependencies"""
    return AuthService(
        mock_users_repository,
        mock_sessions_repository,
        mock_password_service,
    )


def test_authenticate_user_success(
    service, mock_password_service, mock_users_repository
):
    """Test successful user authentication."""
    hashed_password = mock_password_service.get_hash("correct_password")
    user = User(id=1, email="test@example.com", hashed_password=hashed_password)
    mock_users_repository.get_by_email.return_value = user

    result = service.authenticate_user("test@example.com", "correct_password")

    assert result == user


def test_authenticate_user_wrong_password(
    service, mock_password_service, mock_users_repository
):
    """Test authentication with wrong password."""
    hashed_password = mock_password_service.get_hash("correct_password")
    user = User(id=1, email="test@example.com", hashed_password=hashed_password)
    mock_users_repository.get_by_email.return_value = user

    result = service.authenticate_user("test@example.com", "wrong_password")

    assert result is None


def test_authenticate_user_not_found(service, mock_users_repository):
    """Test authentication when user is not found."""
    mock_users_repository.get_by_email.return_value = None

    result = service.authenticate_user("nonexistent@example.com", "password")

    assert result is None


@pytest.mark.asyncio
async def test_register_user(service):
    """Test registering a new user through the service"""
    user_create = UserCreate(email="test@example.com", password="password123")

    user = await service.register_user(user_create)

    assert user.id == 1
    assert user.email == "test@example.com"
    assert hasattr(user, "hashed_password")
    assert user.hashed_password != "password123"


def test_login_user_success(
    service, mock_users_repository, mock_sessions_repository, mock_password_service
):
    """Test successful login and session creation."""
    hashed_password = mock_password_service.get_hash("correct_password")
    user = User(id=1, email="test@example.com", hashed_password=hashed_password)
    mock_users_repository.get_by_email.return_value = user

    session_id = UUID("12345678-1234-5678-1234-567812345678")
    session = MagicMock()
    session.id = session_id
    mock_sessions_repository.create.return_value = session

    result = service.login_user("test@example.com", "correct_password")

    assert result == session_id
    mock_sessions_repository.create.assert_called_once_with(user.id, expires_in_days=30)


def test_login_user_invalid_credentials(service, mock_users_repository):
    """Test login with invalid credentials raises ValueError."""
    mock_users_repository.get_by_email.return_value = None

    with pytest.raises(ValueError) as exc:
        service.login_user("nonexistent@example.com", "password")

    assert "Invalid credentials" in str(exc.value)


def test_logout_user(service, mock_sessions_repository):
    """Test user logout invalidates the session."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")

    service.logout_user(session_id)

    mock_sessions_repository.invalidate_by_id.assert_called_once_with(session_id)


def test_get_current_user_valid_session(
    service, mock_users_repository, mock_sessions_repository
):
    """Test getting current user from valid session."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")
    user_id = 1

    session = MagicMock()
    session.user_id = user_id
    mock_sessions_repository.get_active_by_id.return_value = session

    user = User(id=user_id, email="test@example.com", hashed_password="hashed_pass")
    mock_users_repository.get_by_id.return_value = user

    result = service.get_current_user(session_id)

    assert result == user
    mock_sessions_repository.get_active_by_id.assert_called_once_with(session_id)
    mock_users_repository.get_by_id.assert_called_once_with(user_id)


def test_get_current_user_invalid_session(service, mock_sessions_repository):
    """Test getting current user with invalid session raises ValueError."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")
    mock_sessions_repository.get_active_by_id.return_value = None

    with pytest.raises(ValueError) as exc:
        service.get_current_user(session_id)

    assert "Invalid or expired session" in str(exc.value)


def test_get_current_user_user_not_found(
    service, mock_users_repository, mock_sessions_repository
):
    """Test getting current user when user is not found raises ValueError."""
    session_id = UUID("12345678-1234-5678-1234-567812345678")
    user_id = 1

    session = MagicMock()
    session.user_id = user_id
    mock_sessions_repository.get_active_by_id.return_value = session

    mock_users_repository.get_by_id.return_value = None

    with pytest.raises(ValueError) as exc:
        service.get_current_user(session_id)

    assert "User not found" in str(exc.value)
