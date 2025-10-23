from jwt import InvalidTokenError
from pwdlib import PasswordHash

from src.tokens.models import AccessToken
from src.tokens.service import TokensService
from src.users.models import User, UserCreate
from src.users.repository import UsersRepository


class AuthService:
    """
    Service for user operations.
    """

    def __init__(
        self, users_repository: UsersRepository, tokens_service: TokensService
    ):
        """
        Initialize the AuthService.

        Args:
            users_repository: Repository for user data
            tokens_service: Service for token operations
        """
        self.users_repository = users_repository
        self.tokens_service = tokens_service
        self.password_hash = PasswordHash.recommended()

    def get_password_hash(self, password: str) -> str:
        """
        Hash a password.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return self.password_hash.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        return self.password_hash.verify(plain_password, hashed_password)

    def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Authenticate a user by email and password.

        Args:
            email: User's email
            password: User's plain text password

        Returns:
            User if authentication is successful, else None
        """
        user = self.users_repository.get_by_email(email=email)
        if not user:
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        return user

    async def register_user(self, user_create: UserCreate) -> User:
        """
        Register a new user.

        Args:
            user_create: Data for creating a new user

        Returns:
            The created User object
        """
        hashed_password = self.get_password_hash(user_create.password)
        user = User(hashed_password=hashed_password, **user_create.model_dump())

        return self.users_repository.save(user)

    def login_user_and_create_token(self, email: str, password: str) -> AccessToken:
        user = self.authenticate_user(email, password)

        if not user:
            raise ValueError("Incorrect email or password")

        access_token = self.tokens_service.create_access_token(email=user.email)

        return access_token

    def get_current_user_from_token(self, token: str) -> User:
        """
        Get the current user from JWT token.

        Args:
            token: JWT token

        Returns:
            Current user

        Raises:
            ValueError: If token is invalid or user not found
        """
        try:
            email = self.tokens_service.get_email_from_token(token)
        except InvalidTokenError:
            raise ValueError("Could not validate credentials")

        user = self.users_repository.get_by_email(email=email)
        if user is None:
            raise ValueError("Could not validate credentials")

        return user
