from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Role(str, Enum):
    admin = "admin"
    analyst = "analyst"
    user = "user"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    role: Role = Role.user


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
