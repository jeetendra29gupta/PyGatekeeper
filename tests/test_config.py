import importlib

import pytest

import pygatekeeper.config
from pygatekeeper.config import require_env


def test_require_env_success(monkeypatch):
    monkeypatch.setenv("FOO", "bar")
    assert require_env("FOO") == "bar"


def test_require_env_missing(monkeypatch):
    monkeypatch.delenv("FOO", raising=False)
    with pytest.raises(EnvironmentError):
        require_env("FOO")


def test_require_env_empty(monkeypatch):
    monkeypatch.setenv("FOO", "  ")
    with pytest.raises(EnvironmentError):
        require_env("FOO")


@pytest.mark.parametrize(
    "key, value, error_type",
    [
        ("JWT_SECRET_KEY", "", OSError),
        ("JWT_ALGORITHM", "badalg", ValueError),
        ("ACCESS_TOKEN_EXPIRE_MINUTES", "-1", ValueError),
        ("REFRESH_TOKEN_EXPIRE_HOURS", "0", ValueError),
        ("SALT_LENGTH", "4", ValueError),
    ],
)
def test_config_validation(monkeypatch, key, value, error_type):
    monkeypatch.setenv("JWT_SECRET_KEY", "secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    monkeypatch.setenv("REFRESH_TOKEN_EXPIRE_HOURS", "24")
    monkeypatch.setenv("SALT_LENGTH", "12")
    monkeypatch.setenv(key, value)

    with pytest.raises(error_type):
        importlib.reload(pygatekeeper.config)


def test_config_valid(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    monkeypatch.setenv("REFRESH_TOKEN_EXPIRE_HOURS", "24")
    monkeypatch.setenv("SALT_LENGTH", "12")

    importlib.reload(pygatekeeper.config)

    assert pygatekeeper.config.Config.JWT_SECRET_KEY == "secret"
    assert pygatekeeper.config.Config.JWT_ALGORITHM == "HS256"
    assert pygatekeeper.config.Config.ACCESS_TOKEN_EXPIRE_MINUTES == 15
    assert pygatekeeper.config.Config.REFRESH_TOKEN_EXPIRE_HOURS == 24
    assert pygatekeeper.config.Config.SALT_LENGTH == 12


if __name__ == '__main__':
    pytest.main([__file__])
