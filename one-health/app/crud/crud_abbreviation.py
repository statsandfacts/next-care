import logging
from http.client import HTTPException

from sqlalchemy.orm import Session
from app.schemas.user import QuestionAbbreviationMapBase
from app.models.QuestionAbbreviationMap import QuestionAbbreviationMap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_question_abbreviation(db: Session, question: QuestionAbbreviationMapBase):
    try:
        db_obj = QuestionAbbreviationMap()
        db_obj.question_id = question.question_id
        db_obj.question = question.question
        db_obj.answer = question.answer
        db_obj.abbreviation = question.abbreviation
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception as e:
        logger.info("error in creating abbrevation: ", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to ingest data: {str(e)}")
    finally:
        db.close()

def get_question_abbreviation_by_id(
    db: Session, question_id: int, question: str, answer: str
):
    return (
        db.query(QuestionAbbreviationMap)
        .filter(
            QuestionAbbreviationMap.question_id == question_id,
            QuestionAbbreviationMap.question == question,
            QuestionAbbreviationMap.answer == answer
        ).first()
    )


def get_all_question_abbreviations(db: Session):
    return db.query(QuestionAbbreviationMap).all()

def update_question_abbreviation(db: Session, question_id: int, updated_question: str, updated_answer: str, abbreviation: str):
    question = db.query(QuestionAbbreviationMap).filter(QuestionAbbreviationMap.question_id == question_id).first()
    try:
        if question:
            question.question = updated_question
            question.answer = updated_answer
            question.abbreviation = abbreviation
            db.commit()
        return question
    except Exception as e:
        logger.info("error in updating abbrevation: ", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update abbreviation data: {str(e)}")
    finally:
        db.close()


def delete_question_abbreviation(db: Session, question_id: int):
    question = db.query(QuestionAbbreviationMap).filter(QuestionAbbreviationMap.question_id == question_id).first()
    try:
        if question:
            db.delete(question)
            db.commit()
        return question
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete abbreviation data: {str(e)}")
    finally:
        db.close()
