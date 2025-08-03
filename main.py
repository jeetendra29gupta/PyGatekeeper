from pygatekeeper.security import PasswordManager, PasswordError
from pygatekeeper.tokens import TokenManager, TokenError


def password():
    try:
        pm = PasswordManager()

        my_password = "mysecurepassword"
        hashed = pm.hash_password(my_password)
        print(f"Original Password: {my_password}")
        print(f"Hashed Password: {hashed}")

        correct_password = "mysecurepassword"
        assert pm.verify_password(correct_password, hashed)
        if pm.verify_password(correct_password, hashed):
            print(correct_password, " is valid.")

        wrong_password = "wrongpassword"
        assert not pm.verify_password(wrong_password, hashed)
        if not pm.verify_password(wrong_password, hashed):
            print(wrong_password, " is invalid.")

    except PasswordError as e:
        print(f"Password error: {e}")


def token():
    try:
        tm = TokenManager()

        access_token = tm.create_access_token("user_id")
        print(f"Access Token: {access_token}")

        refresh_token = tm.create_refresh_token("user_id")
        print(f"Refresh Token: {refresh_token}")

        claims_access = tm.validate_access_token(access_token)
        print(f"Claims Access: {claims_access}")

        claims_refresh = tm.validate_refresh_token(refresh_token)
        print(f"Claims Refresh: {claims_refresh}")

        """
        Validate a refresh token and issue a new access token for the same subject.
        """
        payload = tm.validate_refresh_token(refresh_token)
        subject = payload.get("sub")
        if not subject:
            raise TokenError("Invalid refresh token: missing subject.")
        refresh_access_token = tm.create_access_token(subject)
        print(f"New Access Token from Refresh: {refresh_access_token}")

    except TokenError as e:
        print(f"Token validation error: {e}")


if __name__ == '__main__':
    password()
    print()
    token()
    print()
