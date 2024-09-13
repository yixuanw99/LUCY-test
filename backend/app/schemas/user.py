# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional
from .report import Report

class UserBase(BaseModel):
    name: str
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    birthday: date
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    birthday: date
    is_active: bool = True
    is_admin: bool = False

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class UserWithReports(User):
    reports: List[Report] = []

UserWithReports.model_rebuild()