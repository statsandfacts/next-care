from typing import List

from pydantic.v1 import BaseModel


# class CaseItems:
#     user_first_name: str

class CaseItemBase(BaseModel):
    doctor_id: str
    patient_id: str


class CaseCreate(CaseItemBase):
    doctor_id: str
    patient_id: str


class CaseUpdate(CaseItemBase):
    insights: str
    status: bool
