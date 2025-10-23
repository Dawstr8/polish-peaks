from unittest.mock import MagicMock

import pytest
from jwt import InvalidTokenError

from src.auth.password_service import PasswordService
from src.auth.service import AuthService
from src.auth.tokens_service import TokensService
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
def mock_tokens_service():
    """Create a mock TokensService"""
    return MagicMock(spec=TokensService)


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
    mock_tokens_service: TokensService,
    mock_password_service: PasswordService,
) -> AuthService:
    """Create a AuthService with mocked dependencies"""
    return AuthService(
        mock_users_repository, mock_tokens_service, mock_password_service
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


def test_login_user_and_create_tokens_success(
    service, mock_users_repository, mock_tokens_service, mock_password_service
):
    """Test successful login and token creation."""
    hashed_password = mock_password_service.get_hash("correct_password")
    user = User(id=1, email="test@example.com", hashed_password=hashed_password)
    mock_users_repository.get_by_email.return_value = user

    mock_access_token = MagicMock()
    mock_refresh_token = MagicMock()
    mock_tokens_service.create_access_token.return_value = mock_access_token
    mock_tokens_service.create_refresh_token.return_value = mock_refresh_token

    result = service.login_user_and_create_tokens(
        "test@example.com", "correct_password"
    )

    assert result == (mock_access_token, mock_refresh_token)
    mock_tokens_service.create_access_token.assert_called_once_with(
        email="test@example.com"
    )
    mock_tokens_service.create_refresh_token.assert_called_once_with(
        email="test@example.com"
    )


def test_login_user_and_create_tokens_invalid_credentials(
    service, mock_users_repository
):
    """Test login with invalid credentials raises ValueError."""
    mock_users_repository.get_by_email.return_value = None

    with pytest.raises(ValueError) as exc:
        service.login_user_and_create_tokens("nonexistent@example.com", "password")

    assert "Incorrect email or password" in str(exc.value)


def test_get_current_user_from_token_valid(
    service, mock_users_repository, mock_tokens_service
):
    """Test getting current user from valid token."""
    user = User(id=1, email="test@example.com", hashed_password="hash")
    mock_users_repository.get_by_email.return_value = user
    mock_tokens_service.get_email_from_token.return_value = "test@example.com"

    result = service.get_current_user_from_token("valid_token")

    assert result == user
    mock_tokens_service.get_email_from_token.assert_called_once_with("valid_token")


def test_get_current_user_from_token_invalid_token(service, mock_tokens_service):
    """Test getting current user from invalid token raises ValueError."""
    mock_tokens_service.get_email_from_token.side_effect = InvalidTokenError(
        "Invalid token"
    )

    with pytest.raises(ValueError) as exc:
        service.get_current_user_from_token("invalid_token")

    assert str(exc.value) == "Could not validate credentials"


def test_get_current_user_from_token_user_not_found(
    service, mock_users_repository, mock_tokens_service
):
    """Test getting current user when user is not found raises ValueError."""
    mock_tokens_service.get_email_from_token.return_value = "test@example.com"
    mock_users_repository.get_by_email.return_value = None

    with pytest.raises(ValueError) as exc:
        service.get_current_user_from_token("valid_token")

    assert str(exc.value) == "Could not validate credentials"


def test_refresh_access_token_success(service, mock_tokens_service):
    """Test refreshing access token with valid refresh token."""
    refresh_token = "valid_refresh_token"
    email = "test@example.com"
    new_access_token = "new_access_token"

    mock_tokens_service.get_email_from_token.return_value = email
    mock_tokens_service.create_access_token.return_value = new_access_token

    result = service.refresh_access_token(refresh_token)

    assert result == new_access_token
    mock_tokens_service.get_email_from_token.assert_called_once_with(refresh_token)
    mock_tokens_service.create_access_token.assert_called_once_with(email=email)


def test_refresh_access_token_invalid_token(service, mock_tokens_service):
    """Test refreshing access token with invalid refresh token raises ValueError."""
    refresh_token = "invalid_refresh_token"

    mock_tokens_service.get_email_from_token.side_effect = InvalidTokenError(
        "Invalid token"
    )

    with pytest.raises(ValueError) as exc:
        service.refresh_access_token(refresh_token)

    assert str(exc.value) == "Could not validate credentials"
