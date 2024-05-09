# Routers/questionnaire_router.py
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List
from app.crud.master_questionnaire import ingest_data, get_all_questionnaires, update_questionnaire, \
    delete_questionnaire, get_questions_by_ids
from app.crud.crud_abbreviation import delete_question_abbreviation, update_question_abbreviation, get_all_question_abbreviations, \
    get_question_abbreviation_by_id, create_question_abbreviation
#from app.database.deps import SessionLocal
from app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.orm import Session,sessionmaker
from app.api import deps
from starlette.responses import JSONResponse
from app.schemas.user import QuestionAbbreviationMapBase, QuestionAbbreviationMapCreate

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


@router.post("/add-abbreviation/")
def create_question_abbreviations(question: QuestionAbbreviationMapBase, db: Session = Depends(get_db)):
    try:
        create_question_abbreviation(db, question)
        return JSONResponse(content={"message": "abbreviations added successfully", "status": 200}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"detail": "Error in adding record", "status": 500}, status_code=500)


@router.get("/get-abbreviation/")
def get_question_abbreviation_by_question(
        question_id: int,
        question: str,
        answer: str,
        db: Session = Depends(deps.get_db)
):
    try:
        # Fetch the record from the database
        record = get_question_abbreviation_by_id(db, question_id, question, answer)

        # If record not found, raise HTTPException
        if not record:
            raise HTTPException(status_code=404, detail="Question abbreviation not found")

        # Manually serialize the record
        record_dict = {
            "question_id": record.question_id,
            "question": record.question,
            "answer": record.answer,
            # Add more fields as needed
        }

        # Return the record as JSON response
        return JSONResponse(content={"question_abbreviation": record_dict, "status": 200}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)

@router.get("/abbreviation/all", response_model=List[QuestionAbbreviationMapBase])
def read_all_questionss(db: Session = Depends(get_db)):
    abbreviations = [abbrev.to_dict() for abbrev in get_all_question_abbreviations(db)]
    return JSONResponse(content={"abbreviations": abbreviations, "status": 200}, status_code=200)

@router.put("/update-abbreviation/", response_model=QuestionAbbreviationMapBase)
def update_question(question_id: int, updated_question: str, updated_answer: str, abbreviation: str, db: Session = Depends(get_db)):
    try:
        question = update_question_abbreviation(db, question_id, updated_question, updated_answer, abbreviation)
        if not question:
            return JSONResponse(content={"message": "No abbreviation data found for this request", "status": 400}, status_code=400)
        return JSONResponse(content={"message": "abbreviations updated successfully", "status": 200}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"detail": "Error in updating abbriviation", "status": e.status_code}, status_code=e.status_code)

@router.delete("/delete-abbreviation/")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    try:
        question = delete_question_abbreviation(db, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return JSONResponse(content={"message": "abbreviations deleted successfully", "status": 200}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)
