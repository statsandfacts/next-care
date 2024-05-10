from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP

Base = declarative_base()

class LevelValueMapping(BaseModel):
    level_id: str
    level_type: str
    allowed_values: list[str]


# Define SQLAlchemy model
class LevelValueMappingDB(Base):
    __tablename__ = 'level_value_mapping'

    level_id = Column(String, primary_key=True)
    level_type = Column(String, primary_key=True)
    allowed_value = Column(String, primary_key=True)
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

