from typing import Protocol

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> User | None:
        ...

    def get_by_email(self, email: str) -> User | None:
        ...

    def get_by_username(self, username: str) -> User | None:
        ...

    def list_users(self, skip: int = 0, limit: int = 50) -> list[User]:
        ...

    def create_user(self, data: UserCreate) -> User:
        ...

    def update_user(self, user: User, data: UserUpdate) -> User:
        ...

    def delete_user(self, user: User) -> None:
        ...
