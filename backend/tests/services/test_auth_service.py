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
