from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.services.auth_service import (
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user_by_username,
)


def test_service_imports():
    assert callable(get_user_by_username)
    assert callable(get_user_by_email)
    assert callable(create_user)
    assert callable(authenticate_user)


@patch("app.services.auth_service.hash_password")
@patch("app.services.auth_service.get_user_by_email")
@patch("app.services.auth_service.get_user_by_username")
def test_create_user_success(
    mock_get_username,
    mock_get_email,
    mock_hash_password,
):
    db = MagicMock()

    user_data = SimpleNamespace(
        username="testuser",
        email="test@example.com",
        password="Password123!",
    )

    mock_get_username.return_value = None
    mock_get_email.return_value = None
    mock_hash_password.return_value = "hashed-password"

    user = create_user(db, user_data)

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed-password"

    db.add.assert_called_once_with(user)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)


@patch("app.services.auth_service.get_user_by_username")
def test_create_user_duplicate_username(mock_get_username):
    db = MagicMock()

    user_data = SimpleNamespace(
        username="existinguser",
        email="new@example.com",
        password="Password123!",
    )

    mock_get_username.return_value = SimpleNamespace(
        username="existinguser"
    )

    with pytest.raises(
        ValueError,
        match="Username already exists",
    ):
        create_user(db, user_data)

    db.add.assert_not_called()
    db.commit.assert_not_called()


@patch("app.services.auth_service.get_user_by_email")
@patch("app.services.auth_service.get_user_by_username")
def test_create_user_duplicate_email(
    mock_get_username,
    mock_get_email,
):
    db = MagicMock()

    user_data = SimpleNamespace(
        username="newuser",
        email="existing@example.com",
        password="Password123!",
    )

    mock_get_username.return_value = None
    mock_get_email.return_value = SimpleNamespace(
        email="existing@example.com"
    )

    with pytest.raises(
        ValueError,
        match="Email already exists",
    ):
        create_user(db, user_data)

    db.add.assert_not_called()
    db.commit.assert_not_called()


@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.get_user_by_username")
def test_authenticate_user_success(
    mock_get_username,
    mock_verify_password,
):
    db = MagicMock()

    expected_user = SimpleNamespace(
        username="testuser",
        hashed_password="hashed-password",
    )

    mock_get_username.return_value = expected_user
    mock_verify_password.return_value = True

    user = authenticate_user(
        db,
        "testuser",
        "Password123!",
    )

    assert user is expected_user

    mock_verify_password.assert_called_once_with(
        "Password123!",
        "hashed-password",
    )


@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.get_user_by_username")
def test_authenticate_user_invalid_password(
    mock_get_username,
    mock_verify_password,
):
    db = MagicMock()

    mock_get_username.return_value = SimpleNamespace(
        username="testuser",
        hashed_password="hashed-password",
    )
    mock_verify_password.return_value = False

    user = authenticate_user(
        db,
        "testuser",
        "WrongPassword",
    )

    assert user is None


@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.get_user_by_username")
def test_authenticate_user_unknown_username(
    mock_get_username,
    mock_verify_password,
):
    db = MagicMock()

    mock_get_username.return_value = None

    user = authenticate_user(
        db,
        "missinguser",
        "Password123!",
    )

    assert user is None
    mock_verify_password.assert_not_called()
