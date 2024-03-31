from sqlalchemy import Column, String, func, ForeignKey
import datetime

from app.db.base_class import Base
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from uuid import uuid4

class UserUpload(Base):
    """
       Database Model for an application Doctor cases
       """
    __tablename__ = "upload_output_table"
    image_id = Column(CHAR(36), primary_key=True, index=True, default=uuid4)
    user_id = Column(
        CHAR(36),
        ForeignKey("user.user_id"),
        nullable=False,
    )
    case_id = Column(
        CHAR(36),
        ForeignKey("Doctor.case_id"),
        nullable=False,
    )
    image_path = Column(String(255), index=True)
    image_output_label = Column(String(500), index=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="user_upload", uselist=False)
    doctor = relationship("Doctor", back_populates="user_uploads", uselist=False)