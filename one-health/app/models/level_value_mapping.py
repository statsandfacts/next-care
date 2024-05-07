from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker

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
