import logging
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from typing import Any, List, Optional
from app.api.deps import get_db
from app.schemas.user import CaseCreate, CaseUpdate, CasePage, CaseReport, DiagnosisMedicineReport
from app import crud, models, schemas
from fastapi.responses import JSONResponse
from app.models.doctor import Doctor
from app.schemas.doctor_txn import DoctorTransactionRequest, DoctorTransactionResponse, UpdateDoctorTransactionRequest, \
    PaginationDoctorTxns
from app.schemas.fee import CreateFeeRequest, UpdateFeeRequest
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
        case = crud.casez.get_by_case_id(db, case_id=case_update_details.case_id)
        if not case:
            raise HTTPException(
                status_code=404,
                detail="The case does not exist in the system",
            )
        crud.casez.update_case(db, db_obj=case, obj_in=case_update_details)
        return JSONResponse(content={"message": "Updated user details successfully", "status": 200},
                            status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)


@router.post("/create-case")
def create_case(case_details: CaseCreate, db: Session = Depends(get_db)
                ) -> Any:
    try:
        # if (crud.casez.get_by_patient_user_id(db, user_id = case_details.patient_id)) is not None:
        #     raise HTTPException(
        #         status_code=409,
        #         detail="The user already has a case created",
        #     )
        crud.casez.create(db, obj_in=case_details)
        return JSONResponse(content={"message": "Case created successfully", "status": 200}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)


@router.get("/prescription", response_model=DiagnosisMedicineReport)
def get_prescription(
        case_id: str,
        db: Session = Depends(get_db),
) -> Any:
    try:
        case = crud.casez.get_prescription(db, case_id=case_id)
        return case
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)


@router.get("/case-report", response_model=CaseReport)
def case_report(
        case_id: str,
        db: Session = Depends(get_db),
) -> Any:
    try:
        case = crud.casez.get_case_report(db, case_id=case_id)
        return case
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)


@router.get("/case-details", response_model=CasePage)
def read_by_case_id(
        case_id: str,
        db: Session = Depends(get_db),
) -> Any:
    try:
        case = crud.casez.get_by_case_id(db, case_id=case_id)
        patient_user_id = case.patient_user_id if case else None
        user_session = crud.user_session.get_by_user_id(db, user_id=patient_user_id)
        if not case:
            raise HTTPException(
                status_code=404,
                detail="The case does not exist in the system",
            )
        session_id = user_session.session_id if user_session else None

        # Create a CasePage object including session_id
        case_page = CasePage(
            doctor_user_id=case.doctor_user_id,
            patient_user_id=case.patient_user_id,
            insights=case.insights,
            status=case.status,
            session_id=session_id,
            created_at=case.created_at.strftime("%B %d, %Y"),
            doctor_edit_image_insights=case.doctor_edit_image_insights,
            remarks=case.remarks
        )

        return case_page
        #return JSONResponse(content={"user": case, "status": 200}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)


@router.post("/transaction/create-doctor-transaction")
def create_case(txn_details: DoctorTransactionRequest, db: Session = Depends(get_db)
                ) -> Any:
    return crud.doctor_transaction.create_doctor_transaction(db, obj_in=txn_details)


@router.put("/transaction/update-doctor-transaction")
def create_case(txn_details: UpdateDoctorTransactionRequest, db: Session = Depends(get_db)
                ) -> Any:
    return crud.doctor_transaction.create_doctor_transaction(db, obj_in=txn_details)


@router.get("/transaction/get-doctor-transactions", response_model=PaginationDoctorTxns)
def get_doctor_txns(user_id: str, order_by_field: Optional[str] = 'updated_at',
                    order_by_direction: Optional[str] = 'asc',
                    db: Session = Depends(get_db),
                    page: int = Query(default=1, ge=1),
                    limit: int = Query(default=10, ge=1)):
    skip = (page - 1) * limit
    return crud.doctor_transaction.get_doc_txn_per_id(db, user_id=user_id, skip=skip, limit=limit,
                                                      order_by_field=order_by_field,
                                                      order_by_direction=order_by_direction)


@router.get("/transaction/get-case-transactions", response_model=PaginationDoctorTxns)
def get_case_txns(case_id: Optional[str] = None, order_by_field: Optional[str] = 'updated_at',
                  order_by_direction: Optional[str] = 'asc',
                  db: Session = Depends(get_db),
                  page: int = Query(default=1, ge=1),
                  limit: int = Query(default=10, ge=1)):
    skip = (page - 1) * limit
    return crud.doctor_transaction.get_doc_txn_per_case(db, case_id=case_id, skip=skip, limit=limit,
                                                        order_by_field=order_by_field,
                                                        order_by_direction=order_by_direction)


@router.post("/transaction/create-case-fee")
def create_case_fee(txn_details: CreateFeeRequest, db: Session = Depends(get_db)
                    ) -> Any:
    return crud.consulting_fee.create_fee(db, obj_in=txn_details)


@router.put("/transaction/update-case-fee")
def update_case_fee(txn_details: UpdateFeeRequest, db: Session = Depends(get_db)
                ) -> Any:
    return crud.consulting_fee.create_fee(db, obj_in=txn_details)

@router.get("/transaction/get-case-fee/all")
def get_all_case_fee(db: Session = Depends(get_db)):
    return crud.consulting_fee.get_all_fee(db)

@router.get("/transaction/get-case-fee")
def get_case_fee_by_user(user_id : str, db: Session = Depends(get_db)):
    return crud.consulting_fee.get_fee_by_user(db, user_id=user_id)

@router.delete("/transaction/delete-case-fee")
def delete_case_fee(user_id : str, db: Session = Depends(get_db)):
    return crud.consulting_fee.delete_fee(db, user_id=user_id)

