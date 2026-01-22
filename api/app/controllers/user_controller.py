from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.helpers.pagination import clamp_limit
from app.requests.user_request import UserCreateRequest, UserUpdateRequest
from app.resources.user_resource import UserResource
from app.services import user_service
from app.services.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
    UsernameAlreadyExistsError,
)


class UserController:
    def list_users(self, db: Session, skip: int = 0, limit: int = 50):
        safe_limit = clamp_limit(limit)
        users = user_service.list_users(db, skip=skip, limit=safe_limit)
        return UserResource.list(users)

    def get_user(self, db: Session, user_id: int):
        try:
            user = user_service.get_user(db, user_id)
            return UserResource.from_model(user)
        except UserNotFoundError as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc

    def create_user(self, db: Session, payload: UserCreateRequest):
        try:
            user = user_service.create_user(db, payload)
            return UserResource.from_model(user)
        except EmailAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail="Email already exists") from exc
        except UsernameAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail="Username already exists") from exc

    def update_user(self, db: Session, user_id: int, payload: UserUpdateRequest):
        try:
            user = user_service.update_user(db, user_id, payload)
            return UserResource.from_model(user)
        except UserNotFoundError as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc
        except EmailAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail="Email already exists") from exc
        except UsernameAlreadyExistsError as exc:
            raise HTTPException(status_code=409, detail="Username already exists") from exc

    def delete_user(self, db: Session, user_id: int) -> None:
        try:
            user_service.delete_user(db, user_id)
        except UserNotFoundError as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc
