# Routers/questionnaire_router.py
from fastapi import APIRouter, HTTPException
from typing import Dict
from app.crud.master_questionnaire import ingest_data, get_all_questionnaires, update_questionnaire, \
    delete_questionnaire, get_questions_by_ids
#from app.database.deps import SessionLocal
from app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.orm import Session,sessionmaker
from app.api import deps
from starlette.responses import JSONResponse

router = APIRouter(prefix="/master_questionnaire", tags=["master_questionnaire"])

@router.post("/add_questionnaire/")
async def ingest_questionnaire(data: Dict, db: Session = Depends(deps.get_db)):
    try:
        ingest_data(data,db)
        return JSONResponse(content={"message": "Data ingested successfully", "status": 200}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest data: {str(e)}")


@router.get("/get_questionnaires/")
def get_questionnaires(db: Session = Depends(deps.get_db)):
    try:
        questionnaires = get_all_questionnaires(db)
        return JSONResponse(content={"questionnaires": questionnaires, "status": 200}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch questionnaires: {str(e)}")


@router.put("/update_questionnaire/{question_id}")
def update_questionnaire_detail(question_id: int, updated_data: dict, db: Session = Depends(deps.get_db)):
    try:
        update_questionnaire(question_id, updated_data, db)
        return JSONResponse(content={"message": "Questionnaire updated successfully", "status": 200}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update questionnaire: {str(e)}")


@router.delete("/delete_questionnaire/{question_id}")
def delete_questionnaire_details(question_id: int, db: Session = Depends(deps.get_db)):
    try:
        delete_questionnaire(question_id, db)
        return JSONResponse(content={"message": f"Questionnaire with ID {question_id} deleted successfully", "status": 200}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete questionnaire: {str(e)}")


@router.post("/show_question_details/")
def get_questions_by_ids_details(question_ids: dict, db: Session = Depends(deps.get_db)):
    try:
        questions = get_questions_by_ids(question_ids['question_ids'], db)
        return JSONResponse(
            content={"questions": questions, "status": 200},
            status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch questions: {str(e)}")