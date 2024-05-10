from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer,Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP

Base = declarative_base()

class MasterQuestionnaire(Base):
    __tablename__ = 'master_questionnaire'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    question_type = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    multiple_selection_allowed = Column(Boolean, nullable=False)
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

    question_values = relationship("QuestionValue", back_populates="master_questionnaire")

class QuestionValue(Base):
    __tablename__ = 'question_values'

    value_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('master_questionnaire.question_id'))
    allowed_values = Column(String(255), nullable=False)

    master_questionnaire = relationship("MasterQuestionnaire", back_populates="question_values")