from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.crud import user as crud_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud_user.list_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    exists = crud_user.get_by_email(db, str(payload.email))
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")
    return crud_user.create_user(db, payload)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = crud_user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # optional uniqueness check if changing email
    if payload.email is not None:
        exists = crud_user.get_by_email(db, str(payload.email))
        if exists and exists.id != user_id:
            raise HTTPException(status_code=409, detail="Email already exists")
    return crud_user.update_user(db, user, payload)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.delete_user(db, user)
    return None
