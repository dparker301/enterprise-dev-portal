from jose import jwt

from app.core.config import settings
from app.security.jwt import create_access_token, verify_access_token


def test_create_access_token():
    token = create_access_token(
        {"sub": "admin"}
    )

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == "admin"


def test_verify_access_token():
    token = create_access_token(
        {"sub": "admin"}
    )

    username = verify_access_token(token)

    assert username == "admin"


def test_verify_invalid_access_token():
    username = verify_access_token(
        "invalid-token"
    )

    assert username is None
