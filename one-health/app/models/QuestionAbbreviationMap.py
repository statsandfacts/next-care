from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP

Base = declarative_base()

class QuestionAbbreviationMap(Base):
    __tablename__ = 'Question_Abbreviation_Map'

    question_id = Column(Integer, primary_key=True)
    question = Column(String(255))
    answer = Column(String(255))
    abbreviation = Column(String(255))
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

    def to_dict(self):
        return {
            'question_id': self.question_id,
            'question': self.question,
            'answer': self.answer,
            'abbreviation': self.abbreviation
        }
