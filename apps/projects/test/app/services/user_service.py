from sqlalchemy.orm import Session

from app.models.user import User
from app.events.dispatcher import dispatcher
from app.events.user_events import USER_CREATED
from app.repositories import user_repository
from app.schemas.user import UserCreate, UserUpdate
from app.services.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
    UsernameAlreadyExistsError,
)


def list_users(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    return user_repository.list_users(db, skip=skip, limit=limit)


def get_user(db: Session, user_id: int) -> User:
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    return user


def create_user(db: Session, payload: UserCreate) -> User:
    exists = user_repository.get_by_email(db, str(payload.email))
    if exists:
        raise EmailAlreadyExistsError()
    existing_username = user_repository.get_by_username(db, payload.username)
    if existing_username:
        raise UsernameAlreadyExistsError()
    user = user_repository.create_user(db, payload)
    dispatcher.dispatch(USER_CREATED, user=user)
    return user


def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    if payload.email is not None:
        exists = user_repository.get_by_email(db, str(payload.email))
        if exists and exists.id != user_id:
            raise EmailAlreadyExistsError()
    if payload.username is not None:
        exists = user_repository.get_by_username(db, payload.username)
        if exists and exists.id != user_id:
            raise UsernameAlreadyExistsError()
    return user_repository.update_user(db, user, payload)


def delete_user(db: Session, user_id: int) -> None:
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    user_repository.delete_user(db, user)
