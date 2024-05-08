from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QuestionAbbreviationMap(Base):
    __tablename__ = 'Question_Abbreviation_Map'

    question_id = Column(Integer, primary_key=True)
    question = Column(String(255))
    answer = Column(String(255))
    abbreviation = Column(String(255))

    def to_dict(self):
        return {
            'question_id': self.question_id,
            'question': self.question,
            'answer': self.answer,
            'abbreviation': self.abbreviation
        }
