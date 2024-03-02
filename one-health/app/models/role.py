from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mysql import CHAR


class Role(Base):
    __tablename__ = "role"
    role_id = Column(
        CHAR(36), primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text)
