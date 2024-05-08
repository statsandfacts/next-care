from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer,Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List,Optional
Base = declarative_base()

class QuestionSequenceLayout(BaseModel):
    KC1: Optional[str] = None
    KC2: Optional[str] = None
    KC3: Optional[str] = None
    KC4: Optional[str] = None
    KC5: Optional[str] = None
    KC6: Optional[str] = None
    KC7: Optional[str] = None
    KC8: Optional[str] = None
    KC9: Optional[str] = None
    KC10: Optional[str] = None
    question_sequence_Array: list[dict[str, int]]

class QuestionSequenceLayoutDB(Base):
    __tablename__ = 'Question_sequence_layout'

    KC1 = Column(String(255))
    KC2 = Column(String(255))
    KC3 = Column(String(255))
    KC4 = Column(String(255))
    KC5 = Column(String(255))
    KC6 = Column(String(255))
    KC7 = Column(String(255))
    KC8 = Column(String(255))
    KC9 = Column(String(255))
    KC10 = Column(String(255))
    question_id = Column(Integer)
    sequence = Column(Integer, primary_key=True)
    key_combination = Column(String(255), primary_key=True)

    def to_dict(self):
        return {
            'KC1': self.KC1,
            'KC2': self.KC2,
            'KC3': self.KC3,
            'KC4': self.KC4,
            'KC5': self.KC5,
            'KC6': self.KC6,
            'KC7': self.KC7,
            'KC8': self.KC8,
            'KC9': self.KC9,
            'KC10': self.KC10,
            'question_id': self.question_id,
            'sequence': self.sequence,
            'key_combination': self.key_combination
            # Include other attributes here
        }