from sqlalchemy import select
from sqlalchemy.orm import Session

from app.helpers.passwords import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalars().first()

def get_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalars().first()


def list_users(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def create_user(db: Session, data: UserCreate) -> User:
    user = User(
        name=data.name,
        email=str(data.email),
        username=data.username,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    if data.name is not None:
        user.name = data.name
    if data.email is not None:
        user.email = str(data.email)
    if data.username is not None:
        user.username = data.username
    if data.password is not None:
        user.password_hash = hash_password(data.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
