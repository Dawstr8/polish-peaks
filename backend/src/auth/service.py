from jwt import InvalidTokenError

from src.auth.models import Token
from src.auth.password_service import PasswordService
from src.auth.tokens_service import TokensService
from src.users.models import User, UserCreate
from src.users.repository import UsersRepository


class AuthService:
    """
    Service for user operations.
    """

    def __init__(
        self,
        users_repository: UsersRepository,
        tokens_service: TokensService,
        password_service: PasswordService,
    ):
        """
        Initialize the AuthService.

        Args:
            users_repository: Repository for user data
            tokens_service: Service for token operations
            password_service: Service for password hashing and verification
        """
        self.users_repository = users_repository
        self.tokens_service = tokens_service
        self.password_service = password_service

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

        if not self.password_service.verify(password, user.hashed_password):
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
        hashed_password = self.password_service.get_hash(user_create.password)
        user = User(hashed_password=hashed_password, **user_create.model_dump())

        return self.users_repository.save(user)

    def login_user_and_create_tokens(
        self, email: str, password: str
    ) -> tuple[str, str]:
        user = self.authenticate_user(email, password)

        if not user:
            raise ValueError("Incorrect email or password")

        access_token = self.tokens_service.create_access_token(email=user.email)
        refresh_token = self.tokens_service.create_refresh_token(email=user.email)

        return access_token, refresh_token

    def get_email_from_token(self, token: str) -> str:
        """
        Get email from JWT token.

        Args:
            token: JWT token
        Returns:
            Email extracted from the token
        Raises:
            ValueError: If the token is invalid
        """
        try:
            return self.tokens_service.get_email_from_token(token)
        except InvalidTokenError:
            raise ValueError("Could not validate credentials")

    def get_current_user_from_token(self, access_token: str) -> User:
        """
        Get the current user from JWT token.

        Args:
            access_token: JWT token

        Returns:
            Current user

        Raises:
            ValueError: If token is invalid or user not found
        """

        email = self.get_email_from_token(access_token)
        user = self.users_repository.get_by_email(email=email)
        if user is None:
            raise ValueError("Could not validate credentials")

        return user

    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Refresh the access token using a refresh token.

        Args:
            refresh_token: Refresh JWT token

        Returns:
            New access token

        Raises:
            ValueError: If refresh token is invalid
        """
        email = self.get_email_from_token(refresh_token)
        new_access_token = self.tokens_service.create_access_token(email=email)
        return new_access_token
