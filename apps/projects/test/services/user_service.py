from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repo
from app.schemas.user import UserCreate, UserUpdate


class UserNotFoundError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass


def list_users(db: Session, *, skip: int = 0, limit: int = 50) -> list[User]:
    return user_repo.list_users(db, skip=skip, limit=limit)


def get_user(db: Session, user_id: int) -> User:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    return user


def create_user(db: Session, payload: UserCreate) -> User:
    if user_repo.get_by_email(db, str(payload.email)):
        raise EmailAlreadyExistsError()
    if user_repo.get_by_username(db, payload.username):
        raise UsernameAlreadyExistsError()
    return user_repo.create_user(db, payload)


def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    if payload.email is not None:
        existing = user_repo.get_by_email(db, str(payload.email))
        if existing and existing.id != user_id:
            raise EmailAlreadyExistsError()
    if payload.username is not None:
        existing = user_repo.get_by_username(db, payload.username)
        if existing and existing.id != user_id:
            raise UsernameAlreadyExistsError()
    return user_repo.update_user(db, user, payload)


def delete_user(db: Session, user_id: int) -> None:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    user_repo.delete_user(db, user)
