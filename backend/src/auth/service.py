from uuid import UUID

from src.auth.password_service import PasswordService
from src.sessions.repository import SessionsRepository
from src.users.models import User, UserCreate
from src.users.repository import UsersRepository


class AuthService:
    """
    Service for user operations.
    """

    def __init__(
        self,
        users_repository: UsersRepository,
        sessions_repository: SessionsRepository,
        password_service: PasswordService,
    ):
        """
        Initialize the AuthService.

        Args:
            users_repository: Repository for user data
            sessions_repository: Repository for session management
            password_service: Service for password hashing and verification
        """
        self.users_repository = users_repository
        self.sessions_repository = sessions_repository
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

    def login_user(self, email: str, password: str) -> UUID:
        """
        Log in a user by authenticating their credentials and creating a new session.

        Args:
            email: User's email
            password: User's plain text password

        Returns:
            UUID of the created session

        Raises:
            ValueError: If credentials are invalid
        """
        user = self.authenticate_user(email, password)
        if not user:
            raise ValueError("Invalid credentials")

        session = self.sessions_repository.create(user.id, expires_in_days=30)
        return session.id

    def logout_user(self, session_id: UUID) -> None:
        """
        Log out a user by invalidating their session.

        Args:
            session_id: UUID of the session to invalidate
        """
        self.sessions_repository.invalidate_by_id(session_id)

    def get_current_user(self, session_id: UUID) -> User:
        """
        Get the current authenticated user from a session ID.

        Args:
            session_id: UUID of the session

        Returns:
            The authenticated User
        Raises:
            ValueError: If session is invalid or expired
        """
        session = self.sessions_repository.get_active_by_id(session_id)
        if not session:
            raise ValueError("Invalid or expired session")

        user = self.users_repository.get_by_id(session.user_id)
        if not user:
            raise ValueError("User not found")

        return user
