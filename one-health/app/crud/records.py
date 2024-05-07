from app.models.question_sequence_layout import QuestionSequenceLayout,QuestionSequenceLayoutDB
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
import hashlib
from app.api import deps
from app.api.deps import get_db
from fastapi import Depends

# CRUD operations
def create_question_sequence_layout(QuestionSequenceLayoutList: List[QuestionSequenceLayout], db: Session):
    # Calculate the key_combination
    try:
        for item in QuestionSequenceLayoutList:
            kc_values = [getattr(item, f"KC{i}", None) for i in range(1, 11)]
            kc_values = [kc if kc is not None else "" for kc in kc_values]
            key_combination = hashlib.md5(''.join(kc_values).encode()).hexdigest()
            for seq_item in item.question_sequence_Array:
                db_sequence_item = QuestionSequenceLayoutDB(
                    KC1=kc_values[0],
                    KC2=kc_values[1],
                    KC3=kc_values[2],
                    KC4=kc_values[3],
                    KC5=kc_values[4],
                    KC6=kc_values[5],
                    KC7=kc_values[6],
                    KC8=kc_values[7],
                    KC9=kc_values[8],
                    KC10=kc_values[9],
                    question_id=seq_item['question_id'],
                    sequence=seq_item['sequence_id'],
                    key_combination=key_combination
                    )
                db.add(db_sequence_item)
                db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def upsert_records(key_combination: str,new_data: QuestionSequenceLayout, db: Session):
    # Calculate the key_combination
    try:
        # Delete existing records for the key
        db.query(QuestionSequenceLayoutDB).filter(
            QuestionSequenceLayoutDB.key_combination == key_combination
        ).delete()
        kc_values = [getattr(new_data, f"KC{i}", None) for i in range(1, 11)]
        kc_values = [kc if kc is not None else "" for kc in kc_values]
        for seq_item in new_data.question_sequence_Array:
                db_sequence_item = QuestionSequenceLayoutDB(
                    KC1=kc_values[0],
                    KC2=kc_values[1],
                    KC3=kc_values[2],
                    KC4=kc_values[3],
                    KC5=kc_values[4],
                    KC6=kc_values[5],
                    KC7=kc_values[6],
                    KC8=kc_values[7],
                    KC9=kc_values[8],
                    KC10=kc_values[9],
                    question_id=seq_item['question_id'],
                    sequence=seq_item['sequence_id'],
                    key_combination=key_combination
                    )
                db.add(db_sequence_item)
                db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def upsert_records(key_combination: str,new_data: QuestionSequenceLayout, db: Session):
    # Calculate the key_combination
    try:
        # Delete existing records for the key
        db.query(QuestionSequenceLayoutDB).filter(
            QuestionSequenceLayoutDB.key_combination == key_combination
        ).delete()
        kc_values = [getattr(new_data, f"KC{i}", None) for i in range(1, 11)]
        kc_values = [kc if kc is not None else "" for kc in kc_values]
        for seq_item in new_data.question_sequence_Array:
                db_sequence_item = QuestionSequenceLayoutDB(
                    KC1=kc_values[0],
                    KC2=kc_values[1],
                    KC3=kc_values[2],
                    KC4=kc_values[3],
                    KC5=kc_values[4],
                    KC6=kc_values[5],
                    KC7=kc_values[6],
                    KC8=kc_values[7],
                    KC9=kc_values[8],
                    KC10=kc_values[9],
                    question_id=seq_item['question_id'],
                    sequence=seq_item['sequence_id'],
                    key_combination=key_combination
                    )
                db.add(db_sequence_item)
                db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def del_records(key_combination: str, db: Session):
    # Calculate the key_combination
    try:
        # Delete existing records for the key
        db.query(QuestionSequenceLayoutDB).filter(
            QuestionSequenceLayoutDB.key_combination == key_combination
        ).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_records(key_combination: str, db: Session):
    try:
        records = db.query(QuestionSequenceLayoutDB).filter(QuestionSequenceLayoutDB.key_combination == key_combination).all()
        if not records:
            raise HTTPException(status_code=404, detail="No records found for the provided key_combination")
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
