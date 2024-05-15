from sqlalchemy import Column, String, func, event
import datetime

from app.db.base_class import Base
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP
from sqlalchemy.orm import relationship, Session
from uuid import uuid4
from app.db.session import SessionLocal


class Doctor(Base):
    """
       Database Model for an application Doctor cases
       """
    __tablename__ = "Doctor"
    case_id = Column(CHAR(36), primary_key=True, index=True)
    sec_case_id = Column(CHAR(36), index=True, default=uuid4)
    doctor_user_id = Column(String(255), index=True)
    patient_user_id = Column(String(255), index=True)
    insights = Column(String(255), index=True)
    remarks = Column(String(255), index=True)
    status = Column(String(50), index=True)
    doctor_edit_image_insights = Column(String(500))
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

    user_uploads = relationship(
        "UserUpload",
        back_populates="doctor",
        primaryjoin="Doctor.case_id == UserUpload.case_id",
        cascade="all, delete-orphan, save-update",
        uselist=False
    )


def generate_case_id(session: Session) -> str:
    prefix = "NXTCR"
    last_case = session.query(Doctor).filter(Doctor.case_id.like(f"{prefix}%")).order_by(Doctor.case_id.desc()).first()

    if last_case:
        last_id = int(last_case.case_id.replace(prefix, ""))
        new_id = last_id + 1
    else:
        new_id = 1

    return f"{prefix}{new_id:013d}"


@event.listens_for(Doctor, "before_insert")
def set_case_id(mapper, connection, target):
    session = SessionLocal()
    try:
        target.case_id = generate_case_id(session)
    finally:
        session.close()



