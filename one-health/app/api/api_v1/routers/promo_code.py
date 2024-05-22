import logging
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from typing import Any, List, Optional
from app.api.deps import get_db
from app.schemas.user import CaseCreate, CaseUpdate, CasePage, CaseReport, DiagnosisMedicineReport
from app import crud, models, schemas
from fastapi.responses import JSONResponse
from app.models.PromoCode import PromoCode
from app.schemas.doctor_txn import DoctorTransactionRequest, DoctorTransactionResponse, UpdateDoctorTransactionRequest, \
    PaginationDoctorTxns
from app.schemas.fee import UpdatePromoCodeRequest
from sqlalchemy.orm import Session

router = APIRouter(prefix="/discount", tags=["promo_code"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/promo-code")
def read_promo_code(promo_code: str, db: Session = Depends(get_db)):
    return crud.promo_code.get_promo_code(db, promo_code)

@router.get("/promo-code/all")
def get_all_case_fee(db: Session = Depends(get_db)):
    return crud.promo_code.get_all_promo_codes(db)

@router.post("/create-promo-code")
def create_promo_code(promo_code: UpdatePromoCodeRequest, db: Session = Depends(get_db)):
    return crud.promo_code.create_promo_code(db, promo_code)

@router.put("/update-promo-code")
def update_promo_code(obj_in: UpdatePromoCodeRequest, db: Session = Depends(get_db)):
    db_obj = db.query(PromoCode).filter(PromoCode.Promo_Code == obj_in.Promo_Code).first()
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return crud.promo_code.update_promo_code(db, db_obj=db_obj, obj_in= obj_in)

@router.delete("/delete-promo-code")
def delete_promo_code(promo_code: str, db: Session = Depends(get_db)):
    db_promo_code = crud.promo_code.get_promo_code(promo_code)
    return crud.promo_code.delete_promo_code(db, db_promo_code)