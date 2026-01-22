from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    username: str | None = None

    class Config:
        from_attributes = True
