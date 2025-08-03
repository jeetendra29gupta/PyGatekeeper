import os

from dotenv import load_dotenv

load_dotenv()


def require_env(name: str) -> str:
    """Raise an error if a required environment variable is missing or empty."""
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value


class Config:
    # Load and validate environment variables
    JWT_SECRET_KEY: str = require_env("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = require_env("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(require_env("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_HOURS: int = int(require_env("REFRESH_TOKEN_EXPIRE_HOURS"))
    SALT_LENGTH: int = int(require_env("SALT_LENGTH"))

    if SALT_LENGTH < 8:
        raise ValueError("SALT_LENGTH must be at least 8 for security.")

    if JWT_ALGORITHM not in {"HS256", "HS384", "HS512"}:
        raise ValueError(f"Unsupported JWT_ALGORITHM: {JWT_ALGORITHM}")

    if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer.")

    if REFRESH_TOKEN_EXPIRE_HOURS <= 0:
        raise ValueError("REFRESH_TOKEN_EXPIRE_HOURS must be a positive integer.")
