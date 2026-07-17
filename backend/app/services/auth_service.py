from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.security.hashing import hash_password, verify_password


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    if get_user_by_username(db, user.username):
        raise ValueError("Username already exists")

    if get_user_by_email(db, user.email):
        raise ValueError("Email already exists")

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(
    db: Session,
    username: str,
    password: str,
):
    db_user = get_user_by_username(db, username)

    if db_user is None:
        return None

    if not verify_password(password, db_user.hashed_password):
        return None

    return db_user
