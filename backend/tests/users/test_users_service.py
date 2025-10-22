from unittest.mock import MagicMock

import pytest

from src.users.models import UserCreate
from src.users.repository import UsersRepository
from src.users.service import UsersService


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
def service(mock_users_repository: UsersRepository) -> UsersService:
    """Create a UsersService with mocked dependencies"""
    return UsersService(mock_users_repository)


@pytest.mark.asyncio
async def test_register_user(service):
    """Test registering a new user through the service"""
    user_create = UserCreate(email="test@example.com", password="password123")

    user = await service.register_user(user_create)

    assert user.id == 1
    assert user.email == "test@example.com"
    assert hasattr(user, "hashed_password")
    assert user.hashed_password != "password123"
