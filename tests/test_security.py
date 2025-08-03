import pytest

from pygatekeeper.security import PasswordManager, PasswordError


def test_hash_and_verify_password_success():
    pm = PasswordManager()
    password = "StrongPass123!"
    hashed = pm.hash_password(password)
    assert isinstance(hashed, str)
    assert pm.verify_password(password, hashed) is True


def test_verify_password_wrong_password():
    pm = PasswordManager()
    password = "CorrectPass"
    wrong_password = "WrongPass"
    hashed = pm.hash_password(password)
    assert pm.verify_password(wrong_password, hashed) is False


def test_verify_password_empty_password():
    pm = PasswordManager()
    password = "SomePass"
    hashed = pm.hash_password(password)
    assert pm.verify_password("", hashed) is False


def test_hash_password_empty_password_raises():
    pm = PasswordManager()
    with pytest.raises(PasswordError):
        pm.hash_password("")


def test_invalid_salt_length_raises():
    with pytest.raises(PasswordError):
        PasswordManager(salt_length=0)


def test_verify_password_invalid_hash_returns_false():
    pm = PasswordManager()
    invalid_hash = "invalidhash"
    assert pm.verify_password("password", invalid_hash) is False


if __name__ == '__main__':
    pytest.main([__file__])
