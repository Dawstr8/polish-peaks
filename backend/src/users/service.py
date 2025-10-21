from pwdlib import PasswordHash

from src.users.models import User, UserCreate
from src.users.repository import UsersRepository


class UsersService:
    """
    Service for user operations.
    """

    def __init__(self, users_repository: UsersRepository):
        """
        Initialize the UsersService.

        Args:
            users_repository: Repository for user data
        """
        self.users_repository = users_repository
        self.password_hash = PasswordHash.recommended()

    def _get_password_hash(self, password: str) -> str:
        """
        Hash a password.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return self.password_hash.hash(password)

    async def register_user(self, user_create: UserCreate) -> User:
        """
        Register a new user.

        Args:
            user_create: Data for creating a new user

        Returns:
            The created User object
        """
        hashed_password = self._get_password_hash(user_create.password)
        user = User(hashed_password=hashed_password, **user_create.model_dump())

        return self.users_repository.save(user)
