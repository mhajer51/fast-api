from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_by_id(db: Session, user_id: int) -> User | None:
    return crud_user.get_by_id(db, user_id)


def get_by_email(db: Session, email: str) -> User | None:
    return crud_user.get_by_email(db, email)


def list_users(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    return crud_user.list_users(db, skip=skip, limit=limit)


def create_user(db: Session, data: UserCreate) -> User:
    return crud_user.create_user(db, data)


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    return crud_user.update_user(db, user, data)


def delete_user(db: Session, user: User) -> None:
    crud_user.delete_user(db, user)
