from datetime import datetime
from typing import Optional, List, Dict, Any

from app.schemas.user_role import UserRole
from pydantic import UUID4, BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email_id: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    first_name: str
    last_name: str
    user_type: str
    government_id: str
    government_idtype: str
    email_id: str
    phone_number: str
    address: str
    qualification: str
    specialization: str


class UserLogin(UserBase):
    password: str
    email_or_phone_no: str
    user_role: str
    session_id: str


class UserLogOut(UserBase):
    user_id: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    user_id: str
    password: str | None = None
    email_id: str | None = None
    phone_number: str | None = None
    address: str | None = None
    qualification: str | None = None
    specialization: str | None = None


class UserInDBBase(UserBase):
    user_id: UUID4
    # user_role: Optional[UserRole]
    created_at: datetime | None = None
    updated_at: datetime | None = None
    address: str | None = None
    qualification: str | None = None
    specialization: str | None = None
    status: str | None = None
    doctor_user_id: str | None = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class PaginatedItemList(BaseModel):
    total: int
    items: List[User]
    #items: List[Dict[str, Any]]
    skip: int
    limit: int


class CaseCreate(BaseModel):
    pass


class CaseUpdate(BaseModel):
    doctor_user_id: str
    patient_user_id: str
    insights: str
    status: bool
    case_id: str

class PaginatedItemDoctorList(BaseModel):
    total: int
    items: List[CaseUpdate]
    skip: int
    limit: int