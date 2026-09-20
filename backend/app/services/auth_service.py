import logging

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.security.hashing import hash_password, verify_password

logger = logging.getLogger(__name__)


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    if get_user_by_username(db, user_data.username):
        raise ValueError("Username already exists")

    if get_user_by_email(db, user_data.email):
        raise ValueError("Email already exists")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(
        "Created user '%s'",
        user.username,
    )

    return user


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User | None:
    user = get_user_by_username(db, username)

    if user is None:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    logger.info(
        "User '%s' authenticated successfully",
        username,
    )

    return user
