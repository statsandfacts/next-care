import json
import logging
from decimal import Decimal
from http.client import HTTPException
from sqlite3 import IntegrityError
from typing import Dict, Any, Union

from sqlalchemy.orm import Session
from app.models import PromoCode
from starlette.responses import JSONResponse
from app.crud.base import CRUDBase
from app.schemas.fee import UpdatePromoCodeRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CRUDPromoCodeService(CRUDBase[PromoCode, UpdatePromoCodeRequest, UpdatePromoCodeRequest]):

    def get_promo_code(self, db: Session, promo_code: str):
        item = db.query(PromoCode).filter(PromoCode.Promo_Code == promo_code).first()
        response_content = json.dumps({"details": item.to_dict()}, cls=CustomJSONEncoder)
        return JSONResponse(
            content={"details": response_content, "status": 200}, status_code=200)

    def get_all_promo_codes(self, db: Session):
        items = db.query(PromoCode).all()
        item_dicts = [item.to_dict() for item in items]
        response_content = json.dumps({"details": item_dicts}, cls=CustomJSONEncoder)
        return JSONResponse(
            content={"details": response_content, "status": 200}, status_code=200)

    def create_promo_code(self, db: Session, promo_code: UpdatePromoCodeRequest):
        new_promocode = PromoCode()
        new_promocode.Promo_Code = promo_code.Promo_Code
        new_promocode.Discount = promo_code.Discount
        new_promocode.Start_Date = promo_code.Start_Date
        new_promocode.End_Date = promo_code.End_Date
        new_promocode.created_by = promo_code.created_by
        db.add(new_promocode)
        db.commit()
        db.refresh(new_promocode)
        return JSONResponse(
            content={"details": "Promocode created successfully", "status": 200}, status_code=200)
        # try:
        #     db.add(promo_code)
        #     db.commit()
        #     db.refresh(promo_code)
        #     return JSONResponse(
        #         content={"details": "Promocode created successfully", "status": 200}, status_code=200)
        # except Exception:
        #     logger.error("Error while promocode to db")
        #     return JSONResponse(
        #         content={"details": "Error while saving promocode", "status": 200}, status_code=200)

    def update_promo_code(
            self,
            db: Session,
            *,
            db_obj: PromoCode,
            obj_in: Union[PromoCode, Dict[str, Any]],
    ) -> PromoCode:
        updated_case = None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        try:
            super().update(db, db_obj=db_obj, obj_in=update_data)
            logger.info("Updated Promo Code")
            return JSONResponse(
                content={"message": "Promocode has been successfully updated", "status": 200},
                status_code=200)
        except IntegrityError as ie:
            logger.error("DB error occured", exc_info=True)
            return JSONResponse(
                content={"detail": str(ie.orig), "status": 500},
                status_code=500)

    def delete_promo_code(self, db: Session, promo_code: PromoCode):
        try:
            db.delete(promo_code)
            db.commit()
            return JSONResponse(
                content={"details": "Promocode has been successfully deleted", "status": 200}, status_code=200)
        except Exception:
            logger.error("Error while deleteing promocode to db")
            return JSONResponse(
                content={"details": "Error while deleteing promocode to db", "status": 500}, status_code=500)

promo_code = CRUDPromoCodeService(PromoCode)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)
