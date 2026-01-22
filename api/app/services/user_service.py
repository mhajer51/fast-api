from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.schemas.user import UserCreate, UserUpdate
from app.services.exceptions import EmailAlreadyExistsError, UserNotFoundError


def list_users(db: Session, skip: int = 0, limit: int = 50):
    return user_repository.list_users(db, skip=skip, limit=limit)


def get_user(db: Session, user_id: int):
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    return user


def create_user(db: Session, payload: UserCreate):
    exists = user_repository.get_by_email(db, str(payload.email))
    if exists:
        raise EmailAlreadyExistsError()
    return user_repository.create_user(db, payload)


def update_user(db: Session, user_id: int, payload: UserUpdate):
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    if payload.email is not None:
        exists = user_repository.get_by_email(db, str(payload.email))
        if exists and exists.id != user_id:
            raise EmailAlreadyExistsError()
    return user_repository.update_user(db, user, payload)


def delete_user(db: Session, user_id: int) -> None:
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    user_repository.delete_user(db, user)
