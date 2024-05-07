from app.models.level_value_mapping import LevelValueMapping, LevelValueMappingDB
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.api.deps import get_db


# Function to ingest data
def create_key_criteria(data: LevelValueMapping, db: Session):
    try:
        for value in data.allowed_values:
            db_record = LevelValueMappingDB(
                level_id=data.level_id,
                level_type=data.level_type,
                allowed_value=value
            )
            db.add(db_record)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to ingest data: {str(e)}")
    finally:
        db.close()


def update_record_by_key(level_id: str, level_type: str, new_allowed_values: list,db: Session):
    try:
        # Delete existing records for the key
        db.query(LevelValueMappingDB).filter(
            LevelValueMappingDB.level_id == level_id
        ).delete()

        # Insert new records with updated values
        for value in new_allowed_values:
            db_record = LevelValueMappingDB(
                level_id=level_id,
                level_type=level_type,
                allowed_value=value
            )
            db.add(db_record)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def delete_record_by_key(level_id: str, db: Session):
    try:
        record_to_delete = db.query(LevelValueMappingDB).filter(
            LevelValueMappingDB.level_id == level_id
        ).first()

        if record_to_delete:
            db.delete(record_to_delete)
            db.commit()
        else:
            raise ValueError("Record not found for deletion")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_all_records(db: Session) -> List[LevelValueMappingDB]:
    try:
        all_records = db.query(LevelValueMappingDB).all()
        return all_records
    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred while fetching all records: {e}")
        raise e
    finally:
        db.close()
