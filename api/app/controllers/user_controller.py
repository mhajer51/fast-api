from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.helpers.pagination import clamp_limit
from app.application.users.service import UserService
from app.events.dispatcher import dispatcher
from app.infrastructure.repositories.user_repository import SqlAlchemyUserRepository
from app.requests.user_request import UserCreateRequest, UserUpdateRequest
from app.resources.user_resource import UserResource
from app.services.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
    UsernameAlreadyExistsError,
)


class UserController:
    def __init__(self, *, event_dispatcher=dispatcher) -> None:
        self.event_dispatcher = event_dispatcher

    def _service(self, db: Session) -> UserService:
        repository = SqlAlchemyUserRepository(db)
        return UserService(repository, event_dispatcher=self.event_dispatcher)

    def list_users(self, db: Session, skip: int = 0, limit: int = 50):
        safe_limit = clamp_limit(limit)
        users = self._service(db).list_users(skip=skip, limit=safe_limit)
        return UserResource.list(users)

    def get_user(self, db: Session, user_id: int):
        try:
            user = self._service(db).get_user(user_id)
            return UserResource.from_model(user)
        except UserNotFoundError as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc

    def create_user(self, db: Session, payload: UserCreateRequest):
        try:
            user = self._service(db).create_user(payload)
            return UserResource.from_model(user)
        except EmailAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail="Email already exists") from exc
        except UsernameAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail="Username already exists") from exc

    def update_user(self, db: Session, user_id: int, payload: UserUpdateRequest):
        try:
            user = self._service(db).update_user(user_id, payload)
            return UserResource.from_model(user)
        except UserNotFoundError as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc
        except EmailAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail="Email already exists") from exc
        except UsernameAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail="Username already exists") from exc

    def delete_user(self, db: Session, user_id: int) -> None:
        try:
            self._service(db).delete_user(user_id)
        except UserNotFoundError as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc
