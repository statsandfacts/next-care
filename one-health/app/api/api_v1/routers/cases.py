import logging
from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Any, List
from app.api.deps import get_db
from app.schemas.user import CaseCreate, CaseUpdate
from app import crud, models, schemas
from fastapi.responses import JSONResponse
from app.models.doctor import Doctor

from sqlalchemy.orm import Session

router = APIRouter(prefix="/case", tags=["case"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.put("/update-case")
def update_case(
            *,
            case_update_details: CaseUpdate,
            db: Session = Depends(get_db)
    ) -> Any:
        """
        Update a case.
        """
        try:
            logger.info("patient user id ------> %s", case_update_details.patient_user_id)
            case = crud.casez.get_by_patient_user_id(db, user_id = case_update_details.patient_user_id)
            if not case:
                raise HTTPException(
                    status_code=404,
                    detail="The case does not exist in the system",
                )
            crud.case.update_case(db, db_obj=case, obj_in=case_update_details)
            return JSONResponse(content={"message": "Updated user details successfully", "status": 200},
                                status_code=200)
        except HTTPException as e:
            return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)


@router.post("/create-case")
def create_case(case_details: CaseCreate, db: Session = Depends(get_db)
                ) -> Any:
    try:
        if (crud.casez.get_by_patient_user_id(db, user_id = case_details.patient_id)) is not None:
            raise HTTPException(
                status_code=409,
                detail="The user already has a case created",
            )
        crud.casez.create(db, obj_in=case_details)
        return JSONResponse(content={"message": "Case created successfully", "status": 200}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)


@router.get("/case-details", response_model=CaseUpdate)
def read_by_case_id(
    case_id: str,
    db: Session = Depends(get_db),
) -> Any:
    try:
        case = crud.casez.get_by_case_id(db, case_id=case_id)
        if not case:
            raise HTTPException(
                status_code=404,
                detail="The case does not exist in the system",
            )
        return case
        #return JSONResponse(content={"user": case, "status": 200}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)
