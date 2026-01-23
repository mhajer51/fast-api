from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.users.repository import UserRepository
from app.helpers.passwords import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalars().first()

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.execute(stmt).scalars().first()

    def list_users(self, skip: int = 0, limit: int = 50) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def create_user(self, data: UserCreate) -> User:
        user = User(
            name=data.name,
            email=str(data.email),
            username=data.username,
            password_hash=hash_password(data.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User, data: UserUpdate) -> User:
        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            user.email = str(data.email)
        if data.username is not None:
            user.username = data.username
        if data.password is not None:
            user.password_hash = hash_password(data.password)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
