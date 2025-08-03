# PyGatekeeper 🔐

**Secure Auth Starts with PyGatekeeper**

PyGatekeeper is a Python-based authentication and access control system designed to provide secure, scalable, and
customizable identity management for modern applications. Whether you're building APIs, web apps, or IoT systems,
PyGatekeeper is your first line of defense.

---

## Features

- ✅ Secure password hashing with bcrypt + random salt
- ✅ JWT-based access and refresh token generation
- ✅ Config-driven validation with environment variable support
- ✅ Stateless authentication
- ✅ Easily extendable for role-based access control (RBAC), OAuth, etc.

---

## Installation

```bash
pip install git+https://github.com/jeetendra29gupta/PyGatekeeper.git
````

Ensure your `.env` or environment variables include:

```env
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_HOURS=24
SALT_LENGTH=12
```

---

## Usage

### 🔐 Password Hashing

```python
from pygatekeeper.security import PasswordManager

pm = PasswordManager()
hashed = pm.hash_password("mysecurepassword")

# Validate
assert pm.verify_password("mysecurepassword", hashed)
assert not pm.verify_password("wrongpassword", hashed)

```

### 🔑 Token Management

```python
from pygatekeeper.tokens import TokenManager

tm = TokenManager()
access_token = tm.create_access_token("user_id")
refresh_token = tm.create_refresh_token("user_id")

# Validate
claims_access = tm.validate_access_token(access_token)
claims_refresh = tm.validate_refresh_token(access_token)
```

---

