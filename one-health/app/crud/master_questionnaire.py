from app.models.master_questionnaire import MasterQuestionnaire,QuestionValue
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api import deps
from app.api.deps import get_db
from fastapi import Depends

def ingest_data(data, db: Session):
    try:
        # Ingest master_questionnaire data
        master_questionnaire_data = data['master_questionnaire']
        master_questionnaire_record = MasterQuestionnaire(
            question_type=master_questionnaire_data['question_type'],
            description=master_questionnaire_data['description'],
            multiple_selection_allowed=master_questionnaire_data['multiple_selection_allowed']
        )
        db.add(master_questionnaire_record)
        db.flush()  # Flush to get the auto-generated question_id

        # Ingest question_values data
        question_values_data = data['question_values']
        for value in question_values_data:
            question_value_record = QuestionValue(
                question_id=master_questionnaire_record.question_id,
                allowed_values=",".join(value['allowed_values'])  # Assuming allowed_values are stored as comma-separated string
            )
            db.add(question_value_record)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_all_questionnaires(db: Session) -> List[dict]:
    questionnaires = db.query(MasterQuestionnaire).all()
    all_data = []
    for questionnaire in questionnaires:
        values = db.query(QuestionValue).filter(QuestionValue.question_id == questionnaire.question_id).all()
        allowed_values = [value.allowed_values for value in values]
        questionnaire_data = {
            "master_questionnaire": {
                "question_id": questionnaire.question_id,
                "question_type": questionnaire.question_type,
                "description": questionnaire.description,
                "multiple_selection_allowed": questionnaire.multiple_selection_allowed
            },
            "question_values": [
                {
                    "value_id": value.value_id,
                    "question_id": value.question_id,
                    "allowed_values": [item for sublist in allowed_values for item in sublist.split(',')]
                } for value in values
            ]
        }
        all_data.append(questionnaire_data)
    return all_data


def update_questionnaire(question_id: int, updated_data: dict, db: Session):
    # Update MasterQuestionnaire
    master_questionnaire = db.query(MasterQuestionnaire).filter(MasterQuestionnaire.question_id == question_id).first()
    if master_questionnaire:
        for key, value in updated_data['master_questionnaire'].items():
            setattr(master_questionnaire, key, value)
    
    # Delete existing QuestionValues for the questionnaire
    db.query(QuestionValue).filter(QuestionValue.question_id == question_id).delete()
    
    # Insert new QuestionValues
    for value in updated_data['question_values']:
        allowed_values = value['allowed_values']
        for allowed_value in allowed_values:
            db.add(QuestionValue(question_id=question_id, allowed_values=allowed_value))
    
    db.commit()
    db.close()

def delete_questionnaire(question_id: int, db: Session):
    # Delete associated QuestionValues
    db.query(QuestionValue).filter(QuestionValue.question_id == question_id).delete()
    # Delete MasterQuestionnaire
    db.query(MasterQuestionnaire).filter(MasterQuestionnaire.question_id == question_id).delete()

    db.commit()
    db.close()

def get_questions_by_ids(question_ids: List[int], db: Session) -> List[dict]:
    questions = db.query(MasterQuestionnaire).filter(MasterQuestionnaire.question_id.in_(question_ids)).all()
    all_data = []
    for question in questions:
        values = db.query(QuestionValue).filter(QuestionValue.question_id == question.question_id).all()
        allowed_values = [value.allowed_values for value in values]
        question_data = {
            "question_id": question.question_id,
            "question_type": question.question_type,
            "allowed_values": allowed_values[0] if allowed_values else [],
            "multiple_val_allowed":question.question_values
        }
        all_data.append(question_data)
    return all_data