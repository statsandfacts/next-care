# Routers/questionnaire_router.py
from fastapi import APIRouter, HTTPException
from typing import Dict
from app.crud.records import create_question_sequence_layout, upsert_records, del_records, get_records
#from app.database.deps import SessionLocal
from app.models.question_sequence_layout import QuestionSequenceLayout, QuestionSequenceLayoutDB
from typing import List
from app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.orm import Session,sessionmaker
from app.api import deps

router = APIRouter(prefix="/records", tags=["records"])


@router.post("/create_records/")
async def cerate_records_seq_layout(data: List[QuestionSequenceLayout], db: Session = Depends(deps.get_db)):
    try:
        create_question_sequence_layout(data, db)
        return {"message": "Data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest data: {str(e)}")


@router.put("/update_records/{key_combination}")
def update_records(key_combination: str, new_data: QuestionSequenceLayout, db: Session = Depends(deps.get_db)):
    try:
        upsert_records(key_combination, new_data, db)
        return {"message": "Record updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update data: {str(e)}")


@router.delete("/delete_records/{key_combination}")
def delete_records(key_combination: str, db: Session = Depends(deps.get_db)):
    try:
        del_records(key_combination, db)
        return {"message": "Record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update data: {str(e)}")

    # Show records endpoint based on key_combination


@router.get("/show_records")
async def show_records(key_combination: str, db: Session = Depends(deps.get_db)):
    try:
        return get_records(key_combination, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update data: {str(e)}")  