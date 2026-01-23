from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.user import UserCreate, UserOut, UserUpdate
from services.user_service import (
    EmailAlreadyExistsError,
    UserNotFoundError,
    UsernameAlreadyExistsError,
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
)

router = APIRouter(prefix="/users")


@router.get("/", response_model=list[UserOut])
def list_all_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return list_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return get_user(db, user_id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, payload)
    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        ) from exc
    except UsernameAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        ) from exc


@router.put("/{user_id}", response_model=UserOut)
def update_user_by_id(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_user(db, user_id, payload)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc
    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        ) from exc
    except UsernameAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        ) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        delete_user(db, user_id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc
    return None
