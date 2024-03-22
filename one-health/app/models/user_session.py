from uuid import uuid4

from sqlalchemy import Column, String, func, ForeignKey, JSON, Boolean
import datetime

from app.db.base_class import Base
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP
class UserSession(Base):
    __tablename__ = "user_session"
    session_id = Column(CHAR(36), index=True, nullable=False)
    user_id = Column(
        CHAR(36),
        nullable=False, primary_key=True
    )
    question_answers = Column(JSON)
    is_active = Column(Boolean(), default=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )