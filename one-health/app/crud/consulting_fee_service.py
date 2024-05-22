import json
import logging
from decimal import Decimal

from sqlalchemy.orm import Session
from app.models.consulting_fee import Consulting_Fee
from app.models.doctor import Doctor
from sqlalchemy.exc import IntegrityError
from app.crud.base import CRUDBase
from fastapi import HTTPException
from typing import Any, Dict, Union
from app.schemas.fee import CreateFeeRequest, UpdateFeeRequest
from starlette.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CRUDConsultingFee(CRUDBase[Consulting_Fee, CreateFeeRequest, UpdateFeeRequest]):

    def create_fee(self, db: Session, obj_in: CreateFeeRequest):
        try:
            db_fee = db.query(Consulting_Fee).filter(Consulting_Fee.user_id == obj_in.user_id).first()
            if not db_fee:
                logger.info("Creating Fee")
                new_fee = Consulting_Fee()
                new_fee.user_id = obj_in.user_id
                new_fee.fee = obj_in.fee
                new_fee.commission = obj_in.commission
                new_fee.user_type = obj_in.user_type
                new_fee.created_by = obj_in.created_by
                new_fee.updated_by = obj_in.updated_by
                db.add(new_fee)
                db.commit()
                db.refresh(new_fee)
                logger.info("Created Fee")
                return JSONResponse(
                    content={"detail": "Doctor transaction has been successfully created", "status": "200"},
                    status_code=200)
            else:
                logger.info("Updating Fee")
                self.update_fee(db, db_obj=db_fee, obj_in=obj_in)
                return JSONResponse(
                    content={"detail": "Doctor transaction has been successfully updated", "status": "200"}, status_code=200)
        except IntegrityError as ie:
            logger.error("DB error occured", exc_info=True)
            return JSONResponse(content={"detail": str(ie.detail), "status": ie.status_code},
                                status_code=ie.status_code)
        except Exception as e:
            logger.error("DB error occured", exc_info=True)
            return JSONResponse(content={"detail": "DB error occured while creating or updating the record.", "status": 500},
                        status_code=500)


    def update_fee(
            self,
            db: Session,
            *,
            db_obj: Consulting_Fee,
            obj_in: Union[CreateFeeRequest, Dict[str, Any]],
    ) -> Consulting_Fee:
        updated_case = None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        try:
            updated_case = super().update(db, db_obj=db_obj, obj_in=update_data)
        except IntegrityError as ie:
            logger.error("DB error occured", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=str(ie.orig)
            )
        logger.info("Updated Fee")
        return updated_case

    def get_all_fee(self, db: Session):
        items = db.query(Consulting_Fee).all()
        item_dicts = [item.to_dict() for item in items]
        response_content = json.dumps({"details": item_dicts}, cls=CustomJSONEncoder)
        return JSONResponse(
            content={"details": response_content, "status": 200}, status_code=200)

    def get_fee_by_user(self, db: Session, user_id: str):
        item =  db.query(Consulting_Fee).filter(Consulting_Fee.user_id == user_id).first()
        response_content = json.dumps({"details": item.to_dict()}, cls=CustomJSONEncoder)
        return JSONResponse(
            content={"details": response_content, "status": 200}, status_code=200)

    def delete_fee(self, db: Session, user_id: str):
        fee = db.query(Consulting_Fee).filter(Consulting_Fee.user_id == user_id).first()
        try:
            if fee:
                db.delete(fee)
                db.commit()
            return JSONResponse(
                content={"message": "Record has been successfully deleted.", "status": 200},status_code=200)
        except Exception as e:
            db.rollback()
            return JSONResponse(
                content={"message": "Error while deleting records.", "status": 500}, status_code=500)
        finally:
            db.close()


consulting_fee = CRUDConsultingFee(Consulting_Fee)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)





