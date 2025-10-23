from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from src.auth.models import Token
from src.config import JWT_SECRET_KEY


class TokensService:
    SECRET_KEY = JWT_SECRET_KEY
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    ALGORITHM = "HS256"

    def encode_data(
        self,
        data: dict,
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
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

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
            return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except InvalidTokenError as e:
            raise InvalidTokenError("Invalid token") from e

    def create_access_token(
        self,
        email: str,
    ) -> Token:
        """
        Create an access token for a user.

        Args:
            email: Email of the user
            expires_delta: Expiration time delta

        Returns:
            Token object containing the JWT token
        """
        access_token = self.encode_data(
            {"sub": email}, timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return Token(access_token=access_token, token_type="bearer")

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
