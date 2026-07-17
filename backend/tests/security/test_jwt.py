from jose import jwt

from app.security.jwt import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)


def test_create_access_token():
    token = create_access_token(
        {"sub": "admin"}
    )

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    assert payload["sub"] == "admin"
