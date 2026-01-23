from app.domain.users.repository import UserRepository
from app.events.dispatcher import dispatcher
from app.events.user_events import USER_CREATED
from app.schemas.user import UserCreate, UserUpdate
from app.services.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
    UsernameAlreadyExistsError,
)


class UserService:
    def __init__(self, repository: UserRepository, *, event_dispatcher=dispatcher) -> None:
        self.repository = repository
        self.event_dispatcher = event_dispatcher

    def list_users(self, skip: int = 0, limit: int = 50):
        return self.repository.list_users(skip=skip, limit=limit)

    def get_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    def create_user(self, payload: UserCreate):
        exists = self.repository.get_by_email(str(payload.email))
        if exists:
            raise EmailAlreadyExistsError()
        existing_username = self.repository.get_by_username(payload.username)
        if existing_username:
            raise UsernameAlreadyExistsError()
        user = self.repository.create_user(payload)
        self.event_dispatcher.dispatch(USER_CREATED, user=user)
        return user

    def update_user(self, user_id: int, payload: UserUpdate):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        if payload.email is not None:
            exists = self.repository.get_by_email(str(payload.email))
            if exists and exists.id != user_id:
                raise EmailAlreadyExistsError()
        if payload.username is not None:
            exists = self.repository.get_by_username(payload.username)
            if exists and exists.id != user_id:
                raise UsernameAlreadyExistsError()
        return self.repository.update_user(user, payload)

    def delete_user(self, user_id: int) -> None:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        self.repository.delete_user(user)
