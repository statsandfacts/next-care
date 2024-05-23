import json
import logging
from decimal import Decimal
from sqlite3 import IntegrityError

from sqlalchemy.orm import Session
from typing import List, Optional, Union, Dict, Any

from app.crud.base import CRUDBase
from app.models.tax import Tax
from app.schemas.tax import TaxCreate, TaxUpdate
from starlette.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CRUDTax(CRUDBase[Tax, TaxCreate, TaxCreate]):
    def get(self, db: Session, service_type: str) -> Optional[Tax]:
        item = db.query(Tax).filter(Tax.Service_Type == service_type).first()
        response_content = json.dumps({"tax": item.to_dict()}, cls=CustomJSONEncoder)
        return response_content

    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> List[Tax]:
        items = db.query(Tax).offset(skip).limit(limit).all()
        item_dicts = [item.to_dict() for item in items]
        response_content = json.dumps({"tax": item_dicts}, cls=CustomJSONEncoder)
        return response_content

    def create(self, db: Session, obj_in: TaxCreate) -> Tax:
        try:
            db_obj = Tax()
            db_obj.Service_Type = obj_in.Service_Type
            db_obj.Tax = obj_in.Tax
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return JSONResponse(
                content={"details": "Tax created successfully", "status": 200}, status_code=200)
        except Exception:
            logger.error("Error while Tax to db")
            return JSONResponse(
                content={"details": "Error while saving Tax", "status": 200}, status_code=200)


    def update_tax(
            self,
            db: Session,
            *,
            db_obj: Tax,
            obj_in: Union[TaxUpdate, Dict[str, Any]],
    ) -> Tax:
        updated_case = None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        try:
            super().update(db, db_obj=db_obj, obj_in=update_data)
            logger.info("Updated Tax")
            return JSONResponse(
                content={"message": "Tax has been successfully updated", "status": 200},
                status_code=200)
        except IntegrityError as ie:
            logger.error("DB error occured", exc_info=True)
            return JSONResponse(
                content={"detail": str(ie.orig), "status": 500},
                status_code=500)

    # def update(self, db: Session, db_obj: Tax, obj_in: TaxUpdate) -> Tax:
    #     if obj_in.Tax is not None:
    #         db_obj.Tax = obj_in.Tax
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    def remove(self, db: Session, service_type: str) -> Tax:
        try:
            db_obj = db.query(Tax).filter(Tax.Service_Type == service_type).first()
            if not db_obj:
                return JSONResponse(
                    content={"details": "Tax not found", "status": 404}, status_code=404)
            db.delete(db_obj)
            db.commit()
            return JSONResponse(
                content={"details": "Tax has been successfully deleted", "status": 200}, status_code=200)
        except Exception:
            logger.error("Error while deleteing tax in db")
            return JSONResponse(
                content={"details": "Error while deleteing tax to db", "status": 500}, status_code=500)

tax = CRUDTax(Tax)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)
