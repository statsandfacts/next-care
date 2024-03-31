import logging
from fastapi import APIRouter, Body, Depends, HTTPException, status
from typing import Any, List
from app.api.deps import get_db
from app import crud, models, schemas
from fastapi.responses import JSONResponse
from app.models.doctor import Doctor
from app.schemas.user import CreateDiagnosis


from sqlalchemy.orm import Session


router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/mapping", response_model=CreateDiagnosis)
def read_mapping(mapping_id: str, db: Session = Depends(get_db)):
    try:
        mapping = crud.diagnosis.get_mapping(db, mapping_id)
        if mapping is None:
            raise HTTPException(status_code=404, detail="Mapping not found")
        mapped_dict = {
            "mapping_id": mapping.mapping_id,
            "visit": mapping.visit,
            "diagnosis": mapping.diagnosis,
            "medicine": mapping.medicine,
            "company": mapping.company,
            "dosage": mapping.dosage,
        }
        return JSONResponse(content={"mappings": mapped_dict, "status": 200}, status_code=200)
        #return mapping

    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)

@router.get("/mappings/", response_model=List[CreateDiagnosis])
def read_all_mappings(db: Session = Depends(get_db)):
    mappings = crud.diagnosis.get_all_mappings(db)
    mapped_dicts = []
    for mapping in mappings:
        mapped_dict = {
            "mapping_id": mapping.mapping_id,
            "visit": mapping.visit,
            "diagnosis": mapping.diagnosis,
            "medicine": mapping.medicine,
            "company": mapping.company,
            "dosage": mapping.dosage,
        }
        mapped_dicts.append(mapped_dict)
    return JSONResponse(content={"mappings": mapped_dicts, "status": 200}, status_code=200)

# @router.get("/mapping", response_model=schemas.User)
# def read_user_by_id(
#     user_id: str,
#     db: Session = Depends(deps.get_db),
# ) -> Any:


@router.post("/mapping")
def create_mapping(diagnose_details: CreateDiagnosis, db: Session = Depends(get_db)
) -> Any:
    try:
        crud.diagnosis.create_mapping(db, diagnose_details.visit, diagnose_details.diagnosis, diagnose_details.medicine,
                                      diagnose_details.company, diagnose_details.dosage)
        return JSONResponse(content={"message": "mapping created successfully", "status": 200}, status_code=200)
    except Exception as ex:
        return JSONResponse(content={"detail": "Error while creating mapping", "status": 500}, status_code=500)



# @router.post("/mapping")
# def create_mapping(visit: str, diagnosis: str, medicine: str, company: str, dosage: str, db: Session = Depends(get_db)):
#     return crud.diagnosis.create_mapping(db, visit, diagnosis, medicine, company, dosage)

@router.put("/update-mapping/{mapping_id}")
def update_mapping(mapping_id: str, diagnose_details: CreateDiagnosis, db: Session = Depends(get_db)):
    try:
        crud.diagnosis.update_mapping(db, mapping_id, diagnose_details.visit, diagnose_details.diagnosis, diagnose_details.medicine,
                                      diagnose_details.company, diagnose_details.dosage)
        return JSONResponse(content={"message": "mapping created successfully", "status": 200}, status_code=200)
    except Exception as ex:
        return JSONResponse(content={"detail": "Error while updating mapping", "status": 500}, status_code=500)



@router.delete("/mapping/{mapping_id}")
def delete_mapping(mapping_id: str, db: Session = Depends(get_db)):
    try:
        crud.diagnosis.delete_mapping(db, mapping_id)
        return JSONResponse(content={"message": "mapping deleted successfully", "status": 200}, status_code=200)
    except HTTPException as ex:
        return JSONResponse(content={"detail": "mapping not found", "status": 500}, status_code=500)


@router.get("/get-diagnosis")
def get_all_diagnosis(db: Session = Depends(get_db)):
    items = crud.diagnosis.get_all_diagnosis(db)
    mapped_dicts = []
    for mapping in items:
        mapped_dict = {
            "diagnosis": mapping.diagnosis,
            "code_id": mapping.code_id
        }
        mapped_dicts.append(mapped_dict)
    return JSONResponse(content={"mappings": mapped_dicts, "status": 200}, status_code=200)