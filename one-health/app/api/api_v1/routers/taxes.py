import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from starlette.responses import JSONResponse

router = APIRouter(prefix="/tax", tags=["promo_code"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/create-tax", response_model=schemas.Tax)
def create_tax(
    tax_in: schemas.TaxCreate, db: Session = Depends(deps.get_db)
):
    tax = crud.tax.create(db=db, obj_in=tax_in)
    return tax

@router.get("/get-tax", response_model=schemas.Tax)
def read_tax(
    service_type: str, db: Session = Depends(deps.get_db)
):
    tax = crud.tax.get(db=db, service_type=service_type)
    if not tax:
        return JSONResponse(
                content={"details": "Tax not found", "status": 404}, status_code=404)
    return JSONResponse(
                content={"tax": tax, "status": 200}, status_code=200)

@router.get("/get-all-tax", response_model=List[schemas.Tax])
def read_taxes(
    skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)
):
    taxes = crud.tax.get_all(db=db, skip=skip, limit=limit)
    return JSONResponse(
        content={"tax": taxes, "status": 200}, status_code=200)

@router.put("/update-tax")
def update_tax(
    tax_in: schemas.TaxUpdate,
    db: Session = Depends(deps.get_db)
):
    tax = db.query(models.Tax).filter(models.Tax.Service_Type == tax_in.Service_Type).first()
    if not tax:
        return JSONResponse(
            content={"details": "Tax not found", "status": 404}, status_code=404)
    tax = crud.tax.update_tax(db, db_obj=tax, obj_in=tax_in)
    return tax

@router.delete("/delete-tax", response_model=schemas.Tax)
def delete_tax(
    service_type: str, db: Session = Depends(deps.get_db)
):
    tax = crud.tax.remove(db=db, service_type=service_type)
    return tax
