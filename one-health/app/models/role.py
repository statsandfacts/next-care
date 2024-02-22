from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mysql import CHAR


class Role(Base):
    role_id = Column(
        CHAR(36), primary_key=True, index=True, default=str(uuid4())
    )
    name = Column(String(100), index=True)
    description = Column(Text)
