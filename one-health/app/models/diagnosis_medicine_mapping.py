from sqlalchemy import Column, String
import datetime

from app.db.base_class import Base
from sqlalchemy.dialects.mysql import CHAR
from uuid import uuid4

class DiagnosisMedicineMapping(Base):
    """
       Database Model for an application DiagnosisMedicineMapping
       """
    __tablename__ = 'diagnosis_medicine_mapping'
    mapping_id =  Column(CHAR(36), primary_key=True, index=True, default=uuid4)
    visit = Column(String, primary_key=True)
    diagnosis = Column(String)
    medicine = Column(String)
    company = Column(String)
    dosage = Column(String)