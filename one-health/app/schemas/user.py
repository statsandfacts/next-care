from typing import Optional, List, Dict, Any, Union

from app.schemas.user_role import UserRole
from pydantic import UUID4, BaseModel, EmailStr, Field
from sqlalchemy import JSON


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
    gender: str
    dob: str
    state: str
    govt_id_image: str
    zipcode: str
    city: str



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
    password: Union[str, None] = None
    email_id: Union[str, None] = None
    phone_number: Union[str, None] = None
    address: Union[str, None] = None
    qualification: Union[str, None] = None
    specialization: Union[str, None] = None
    state: Union[str, None] = None
    govt_id_image: Union[str, None] = None
    zipcode: Union[str, None] = None
    city: Union[str, None] = None
    new_password: Union[str, None] = None
    user_profile_image_path: Union[str, None] = None


class UserInDBBase(UserBase):
    user_id: UUID4
    # user_role: Optional[UserRole]
    # created_at: datetime | None = None
    # updated_at: datetime | None = None
    address: Union[str, None] = None
    qualification: Union[str, None] = None
    specialization: Union[str, None] = None
    status: Union[str, None] = None
    doctor_user_id: Union[str, None] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    dob: Union[str, None] = None
    gender: Union[str, None] = None
    govt_id_image: Union[str, None] = None
    zipcode: Union[str, None] = None
    city: Union[str, None] = None
    new_password: Union[str, None] = None
    user_profile_image_path: Union[str, None] = None


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class PaginatedItemList(BaseModel):
    total: int
    items: List[User]
    # items: List[Dict[str, Any]]
    skip: int
    limit: int


class CaseCreate(BaseModel):
    patient_id: str
    image_path: str


class CaseUpdate(BaseModel):
    doctor_user_id: str
    patient_user_id: str
    insights: Union[str, None] = None
    remarks: Union[str, None] = None
    status: str
    case_id: str
    doctor_edit_image_insights: Union[str, None] = None

class CasePage(BaseModel):
    doctor_user_id: Union[str, None] = None
    patient_user_id: Union[str, None] = None
    insights: Union[str, None] = None
    status: Union[str, None] = None
    case_id: Union[str, None] = None
    session_id: Union[str, None] = None
    created_date: Union[str, None] = None
    remarks: Union[str, None] = None
    doctor_edit_image_insights: Union[str, None] = None


class PaginatedItemDoctorList(BaseModel):
    total: int
    items: List[CasePage]
    skip: int
    limit: int


class SaveUserResponse(BaseModel):
    session_id: str
    user_id: str
    #question_answers: List[Dict[str, Optional[str]]] | None = None
    question_answers: Union[List[Dict[str, Optional[str]]], None] = None


class GetUserResponse(BaseModel):
    question_answers: List[Dict[str, Optional[str]]]


class PatientDashboardResponse(BaseModel):
    case_id: str
    diseases: str
    doctor_name: str
    created_date: str
    case_status: str

class PatientDashboardResponseList(BaseModel):
    cases: List[PatientDashboardResponse]
    status: int

class CreateDiagnosis(BaseModel):
    visit: str
    diagnosis: str
    medicine: str
    company: str
    dosage: str

class ImagePath(BaseModel):
    name: str
    value: Optional[str]


class CaseReport(BaseModel):
    insights: str
    remarks: str
    image_path: List[ImagePath] = Field(..., alias="image_path")
    question_answers: List[Dict[str, Optional[str]]]


class CaseReportResponse(BaseModel):
    case_report: CaseReport = Field(..., alias="case-report")


class DiagnosisMedicine(BaseModel):
    diagnosis: str
    medicine: str
    dosage: str

class DiagnosisMedicineReport(BaseModel):
    patient_name: str
    doctor_name: str
    date: str
    diagnosis_medicines: List[DiagnosisMedicine]


class QuestionAbbreviationMapBase(BaseModel):
    question_id: int
    question: str
    answer: str
    abbreviation: str

class QuestionAbbreviationMapCreate(QuestionAbbreviationMapBase):
    pass

class OtpRequest(BaseModel):
    phone_number: str
    email_id: Union[str, None] = None
