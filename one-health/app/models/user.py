import datetime
from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP
from sqlalchemy.orm import relationship


class User(Base):
    """
    Database Model for an application user
    """
    __tablename__ = "user"
    user_id = Column(
        CHAR(36), primary_key=True, index=True, default=str(uuid4())
    )
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    user_type = Column(String(50), index=True)
    government_id = Column(String(255), index=True)
    government_idtype = Column(String(255), index=True)
    email_id = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(13), unique=True, index=True, nullable=True)
    password = Column(String(255), nullable=False)
    address = Column(String(255), index=True)
    qualification = Column(String(255), index=True)

    specialization = Column(String(255), index=True)
    is_active = Column(Boolean(), default=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


    #user_role = relationship("UserRole", back_populates="user", uselist=False)
    user_role = relationship(
        "UserRole",
        back_populates="user",
        primaryjoin="User.user_id == UserRole.user_id",
        uselist=False
    )
