from app.security.hashing import (
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "MySecurePassword123!"

    hashed = hash_password(password)

    assert hashed != password

    assert verify_password(password, hashed)


def test_invalid_password():
    password = "MySecurePassword123!"
    hashed = hash_password(password)

    assert not verify_password(
        "WrongPassword",
        hashed,
    )
