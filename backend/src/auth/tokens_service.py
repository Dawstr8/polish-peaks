from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from src.auth.models import TokenTypes
from src.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


class TokensService:
    ALGORITHM = "HS256"

    def encode_data(
        self,
        data: dict,
        token_type: TokenTypes,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Create an access token.

        Args:
            data: Data to encode in the token
            expires_delta: Expiration time delta

        Returns:
            Encoded JWT token
        """
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))

        to_encode = data.copy()
        to_encode.update({"exp": expire, "token_type": token_type})

        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_token(self, token: str) -> dict:
        """
        Decode a JWT token.

        Args:
            token: JWT token to decode

        Returns:
            Decoded token data

        Raises:
            InvalidTokenError: If the token is invalid
        """
        try:
            return jwt.decode(token, JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
        except InvalidTokenError as e:
            raise InvalidTokenError("Invalid token") from e

    def create_access_token(self, email: str) -> str:
        """
        Create an access token string for a user.

        Args:
            email: Email of the user
        Returns:
            JWT access token string
        """
        access_token = self.encode_data(
            {"sub": email},
            TokenTypes.ACCESS,
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return access_token

    def create_refresh_token(self, email: str) -> str:
        """
        Create a refresh token string for a user.

        Args:
            email: Email of the user
        Returns:
            JWT refresh token string
        """
        refresh_token = self.encode_data(
            {"sub": email},
            TokenTypes.REFRESH,
            timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return refresh_token

    def get_email_from_token(self, token: str) -> str:
        """
        Extract user email from a JWT token.

        Args:
            token: JWT token

        Returns:
            User email from the token

        Raises:
            InvalidTokenError: If the token is invalid or missing email
        """
        payload = self.decode_token(token)

        email = payload.get("sub")
        if email is None:
            raise InvalidTokenError("Token missing user email")

        return email
