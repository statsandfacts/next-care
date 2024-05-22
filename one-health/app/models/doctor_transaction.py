from sqlalchemy import Column, String, func, ForeignKey
import datetime

from app.db.base_class import Base
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from uuid import uuid4

class Doctor_Transaction(Base):
    """
       Database Model for an application Doctor cases
       """
    __tablename__ = "Doctor_Transaction"
    order_id = Column(CHAR(36), primary_key=True, index=True, default=uuid4)
    user_id = Column(
        CHAR(36),
        nullable=False,
    )
    case_id = Column(
        CHAR(36),
        ForeignKey("Doctor.case_id"),
        nullable=False,
    )
    amount = Column(String(255), index=True)
    paid_type = Column(String(500), index=True)
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

    doctor = relationship("Doctor", back_populates="doc_transaction", uselist=False)