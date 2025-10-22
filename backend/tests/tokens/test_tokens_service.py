from datetime import timedelta

import pytest
from jwt import InvalidTokenError

from src.tokens.models import AccessToken
from src.tokens.service import TokensService


@pytest.fixture
def tokens_service() -> TokensService:
    """Create a TokensService instance for testing."""
    return TokensService()


def test_encode_data_with_expires_delta(tokens_service):
    """Test encoding data with custom expiration delta."""
    data = {"user_id": 1, "email": "test@example.com"}
    expires_delta = timedelta(minutes=30)

    token = tokens_service.encode_data(data, expires_delta)

    assert isinstance(token, str)
    assert len(token) > 0


def test_encode_data_without_expires_delta(tokens_service):
    """Test encoding data without expiration delta (uses default)."""
    data = {"user_id": 1}

    token = tokens_service.encode_data(data)

    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_token_valid(tokens_service):
    """Test decoding a valid JWT token."""
    data = {"user_id": 1, "email": "test@example.com"}
    token = tokens_service.encode_data(data, timedelta(minutes=30))

    decoded = tokens_service.decode_token(token)

    assert decoded["user_id"] == 1
    assert decoded["email"] == "test@example.com"
    assert "exp" in decoded


def test_decode_token_invalid(tokens_service):
    """Test decoding an invalid JWT token raises InvalidTokenError."""
    invalid_token = "invalid.jwt.token"

    with pytest.raises(InvalidTokenError):
        tokens_service.decode_token(invalid_token)


def test_decode_token_expired(tokens_service):
    """Test decoding an expired JWT token raises InvalidTokenError."""
    data = {"user_id": 1}

    token = tokens_service.encode_data(data, timedelta(seconds=-1))

    with pytest.raises(InvalidTokenError):
        tokens_service.decode_token(token)


def test_create_access_token(tokens_service):
    """Test creating an access token for a user."""
    email = "test@example.com"

    access_token = tokens_service.create_access_token(email)

    assert isinstance(access_token, AccessToken)
    assert access_token.token_type == "bearer"
    assert isinstance(access_token.access_token, str)
    assert len(access_token.access_token) > 0


def test_create_access_token_without_expires_delta(tokens_service):
    """Test creating an access token without custom expiration."""
    email = "test@example.com"

    access_token = tokens_service.create_access_token(email)

    assert isinstance(access_token, AccessToken)
    assert access_token.token_type == "bearer"


def test_get_email_from_token_valid(tokens_service):
    """Test extracting email from a valid JWT token."""
    email = "test@example.com"
    access_token = tokens_service.create_access_token(email)

    extracted_email = tokens_service.get_email_from_token(access_token.access_token)

    assert extracted_email == email


def test_get_email_from_token_invalid(tokens_service):
    """Test extracting email from an invalid token raises InvalidTokenError."""
    invalid_token = "invalid.jwt.token"

    with pytest.raises(InvalidTokenError):
        tokens_service.get_email_from_token(invalid_token)


def test_get_email_from_token_missing_sub(tokens_service):
    """Test extracting email from a token missing 'sub' claim raises InvalidTokenError."""
    data = {"some_other_field": "value"}
    token = tokens_service.encode_data(data)

    with pytest.raises(InvalidTokenError):
        tokens_service.get_email_from_token(token)
