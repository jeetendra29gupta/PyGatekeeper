import base64
import os

import bcrypt

from pygatekeeper.config import Config


class PasswordError(Exception):
    """Custom exception for password hashing/verifying errors."""


class PasswordManager:
    def __init__(self, salt_length: int = Config.SALT_LENGTH):
        if salt_length <= 0:
            raise PasswordError("Salt length must be a positive integer.")
        self.salt_length = salt_length

    def _generate_salt(self) -> bytes:
        """Generate a secure random salt."""
        return os.urandom(self.salt_length)

    def hash_password(self, password: str) -> str:
        """
        Hash the given password with a generated salt using bcrypt.

        Returns:
            A base64-encoded string combining the salt and the bcrypt hash.
        """
        if not password:
            raise PasswordError("Password must not be empty.")

        try:
            salt = self._generate_salt()
            salted_password = salt + password.encode('utf-8')
            bcrypt_salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(salted_password, bcrypt_salt)
            combined = salt + hashed
            encoded = base64.b64encode(combined).decode('utf-8')
            return encoded
        except Exception as e:
            raise PasswordError(f"Error hashing password: {e}") from e

    def verify_password(self, password: str, stored_hash: str) -> bool:
        """
        Verify a password against the stored hash.

        Returns:
            True if password matches, False otherwise.
        """
        if not password:
            return False

        try:
            combined = base64.b64decode(stored_hash)
            salt = combined[:self.salt_length]
            hashed = combined[self.salt_length:]
            salted_password = salt + password.encode('utf-8')
            return bcrypt.checkpw(salted_password, hashed)
        except (ValueError, IndexError, TypeError):
            return False
        except Exception as e:
            raise PasswordError(f"Error verifying password: {e}") from e
