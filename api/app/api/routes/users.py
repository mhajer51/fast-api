from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.controllers.user_controller import UserController
from app.requests.user_request import UserCreateRequest, UserUpdateRequest
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])
controller = UserController()


@router.get("/", response_model=list[UserOut])
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return controller.list_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return controller.get_user(db, user_id)


@router.post("/", response_model=UserOut, status_code=201)
def create_user(payload: UserCreateRequest, db: Session = Depends(get_db)):
    return controller.create_user(db, payload)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdateRequest, db: Session = Depends(get_db)):
    return controller.update_user(db, user_id, payload)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    controller.delete_user(db, user_id)
    return None
