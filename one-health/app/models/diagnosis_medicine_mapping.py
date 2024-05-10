from sqlalchemy import Column, String, func
import datetime

from app.db.base_class import Base
from sqlalchemy.dialects.mysql import CHAR
from uuid import uuid4
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP

class DiagnosisMedicineMapping(Base):
    """
       Database Model for an application DiagnosisMedicineMapping
       """
    __tablename__ = 'diagnosis_medicine_mapping'
    mapping_id =  Column(CHAR(36), primary_key=True, index=True, default=uuid4)
    visit = Column(String)
    diagnosis = Column(String)
    medicine = Column(String)
    company = Column(String)
    dosage = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    created_by = Column(CHAR(36), index=True)
    updated_by = Column(CHAR(36), index=True)