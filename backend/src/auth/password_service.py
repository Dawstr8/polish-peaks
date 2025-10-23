from pwdlib import PasswordHash


class PasswordService:
    """
    Service for password hashing and verification.
    """

    def __init__(self):
        """
        Initialize the PasswordService.
        """
        self.password_hash = PasswordHash.recommended()

    def get_hash(self, password: str) -> str:
        """
        Hash a password.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return self.password_hash.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        return self.password_hash.verify(plain_password, hashed_password)
