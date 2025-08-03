import time

import pytest

from pygatekeeper.tokens import TokenManager, TokenError


def test_create_and_validate_access_token():
    tm = TokenManager()
    subject = "user123"
    token = tm.create_access_token(subject)
    assert isinstance(token, str)

    payload = tm.validate_access_token(token)
    assert payload["sub"] == subject
    assert payload["type"] == "access"


def test_create_and_validate_refresh_token():
    tm = TokenManager()
    subject = "user123"
    token = tm.create_refresh_token(subject)
    assert isinstance(token, str)

    payload = tm.validate_refresh_token(token)
    assert payload["sub"] == subject
    assert payload["type"] == "refresh"


def test_access_token_type_mismatch():
    tm = TokenManager()
    token = tm.create_refresh_token("user123")
    with pytest.raises(TokenError, match="Token type mismatch"):
        tm.validate_access_token(token)


def test_refresh_token_type_mismatch():
    tm = TokenManager()
    token = tm.create_access_token("user123")
    with pytest.raises(TokenError, match="Token type mismatch"):
        tm.validate_refresh_token(token)


def test_expired_token_raises(monkeypatch):
    tm = TokenManager()
    subject = "user123"

    # Create token with very short expiry
    token = tm._create_token(subject, exp_seconds=1, token_type="access")
    time.sleep(2)
    with pytest.raises(TokenError, match="expired"):
        tm.validate_access_token(token)


def test_invalid_token_raises():
    tm = TokenManager()
    invalid_token = "this.is.not.a.token"
    with pytest.raises(TokenError, match="Invalid token"):
        tm.validate_access_token(invalid_token)


def test_create_token_with_additional_claims():
    tm = TokenManager()
    subject = "user123"
    extra_claims = {"role": "admin"}
    token = tm.create_access_token(subject, additional_claims=extra_claims)
    payload = tm.validate_access_token(token)
    assert payload["role"] == "admin"


if __name__ == '__main__':
    pytest.main([__file__])
