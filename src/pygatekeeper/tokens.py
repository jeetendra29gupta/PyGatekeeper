import time
from typing import Optional, Dict, Any

import jwt
from jwt import PyJWTError

from pygatekeeper.config import Config


class TokenError(Exception):
    """Custom exception for token errors."""


class TokenManager:
    def __init__(self, config: Config = Config):
        self.secret_key = config.JWT_SECRET_KEY
        self.algorithm = config.JWT_ALGORITHM
        self.access_exp_minutes = config.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_exp_hours = config.REFRESH_TOKEN_EXPIRE_HOURS

    def _current_timestamp(self) -> int:
        return int(time.time())

    def _create_token(self, subject: str, exp_seconds: int, token_type: str,
                      additional_claims: Optional[Dict[str, Any]] = None) -> str:
        """
        General method to create a JWT token.

        Args:
            subject: The identity (user id or username).
            exp_seconds: Expiration duration in seconds.
            token_type: Either "access" or "refresh".
            additional_claims: Optional dict of extra claims.

        Returns:
            Encoded JWT token as string.
        """
        now = self._current_timestamp()
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + exp_seconds,
            "type": token_type,
        }
        if additional_claims:
            payload.update(additional_claims)

        try:
            return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        except PyJWTError as e:
            raise TokenError(f"Failed to create {token_type} token: {e}") from e

    def create_access_token(self, subject: str, additional_claims: Optional[Dict[str, Any]] = None) -> str:
        return self._create_token(subject, self.access_exp_minutes * 60, "access", additional_claims)

    def create_refresh_token(self, subject: str) -> str:
        return self._create_token(subject, self.refresh_exp_hours * 3600, "refresh")

    def _validate_token(self, token: str, expected_type: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise TokenError("Token has expired.")
        except PyJWTError as e:
            raise TokenError(f"Invalid token: {e}") from e

        token_type = payload.get("type")
        if token_type != expected_type:
            raise TokenError(f"Token type mismatch: expected {expected_type}, got {token_type}")

        return payload

    def validate_access_token(self, token: str) -> Dict[str, Any]:
        return self._validate_token(token, "access")

    def validate_refresh_token(self, token: str) -> Dict[str, Any]:
        return self._validate_token(token, "refresh")
