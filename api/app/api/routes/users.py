from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service
from app.services.exceptions import EmailAlreadyExistsError, UserNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return user_service.list_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.get_user(db, user_id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc


@router.post("/", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, payload)
    except EmailAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail="Email already exists") from exc


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    try:
        return user_service.update_user(db, user_id, payload)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc
    except EmailAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail="Email already exists") from exc


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_service.delete_user(db, user_id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc
    return None
