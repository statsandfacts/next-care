import logging

from sqlalchemy.orm import Session
from app.schemas.user import CaseCreate, CaseUpdate
from app.models.doctor import Doctor
from app.models.user_upload import UserUpload
from sqlalchemy.exc import IntegrityError
from app.crud.base import CRUDBase
from fastapi import HTTPException
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import or_, func, and_

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CRUDCase(CRUDBase[Doctor, CaseCreate, CaseUpdate]):

    def get_by_patient_user_id(self, db: Session, *, user_id: str) -> Optional[Doctor]:
        return db.query(self.model).filter(Doctor.patient_user_id == user_id).first()

    def get_by_case_id(self, db: Session, *, case_id: str) -> Optional[Doctor]:
        return db.query(self.model).filter(Doctor.case_id == case_id).first()

    def create(self, db: Session, *, obj_in: CaseCreate) -> Doctor:

        try:
            db_obj = Doctor()
            #db_obj.doctor_user_id = obj_in.doctor_user_id
            db_obj.patient_user_id = obj_in.patient_id
            db_obj.status = 'In Progress'

            #model call
            upload_obj = UserUpload()
            upload_obj.user_id = obj_in.patient_id
            upload_obj.image_path = obj_in.image_path
            upload_obj.image_output_label = "Acne grade 1" #model_output

            db.add(db_obj)
            db.add(upload_obj)
            db.commit()
            db.refresh(db_obj)
        except IntegrityError as ie:
            logger.error("DB error occured", exc_info=True)
            print("dwqdwqdwqd", ie.detail)
            raise HTTPException(
                status_code=500,
                detail=str(ie.orig),
            )
        except Exception as e:
            logger.error("Error creating the case", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Error creating case...",
            )

        return db_obj

    def update_case(
            self,
            db: Session,
            *,
            db_obj: Doctor,
            obj_in: Union[CaseUpdate, Dict[str, Any]],
    ) -> Doctor:
        updated_case = None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        try:
            print("dscsadhcb: ", update_data)
            updated_case = super().update(db, db_obj=db_obj, obj_in=update_data)
        except IntegrityError as ie:
            logger.error("DB error occured", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=str(ie.orig)
            )
        return updated_case

    def get_doctor_list(self, db: Session, status: int, doctor_user_id: str, skip: int = 0, limit: int = 10) -> List[
        Dict]:
        case_items = []
        print("doc id: ", doctor_user_id)
        if not status and not doctor_user_id:
            case_items = db.query(self.model).all()
            print("if case items", case_items)
            item_dicts = [item.__dict__ for item in case_items]
            return item_dicts
        elif not doctor_user_id and status:
            case_items = db.query(self.model).filter(or_(self.model.status == status)).all()
            print("elif case items", case_items)
        else:
            case_items = db.query(self.model). \
                filter(and_(self.model.status == status, self.model.doctor_user_id == doctor_user_id)). \
                all()
            print("else case items", case_items)

        print("case items: ", case_items)
        user_ids = [obj.patient_user_id for obj in case_items]
        print("user ids: ", user_ids)
        # image_path_items = db.query(UserUpload).filter(UserUpload.user_id.in_(user_ids)).all()
        image_path_items = []
        if len(case_items) > 0:
            index = 0
            for item in case_items:
                items = db.query(UserUpload). \
                    filter(UserUpload.user_id == case_items[index].patient_user_id). \
                    filter(func.DATE(UserUpload.created_at) == func.DATE(case_items[index].created_at)). \
                    all()
                print("jfewhbf: ", items)
                if len(items) > 0:
                    image_path_items.append(items[0])
                index = index +1
                print("image_path_items: ", len(image_path_items))


        item_dicts = []

        for case_item in case_items:
            print("case_item.patient_user_id: ", case_item.patient_user_id)
            for image_path_item in image_path_items:

                print("image_path_item.user_id: ", image_path_item.user_id)
                if case_item.patient_user_id == image_path_item.user_id:
                    insights_value = case_item.insights if case_item.insights is not None else ""
                    doctor_user_id_val = case_item.doctor_user_id if case_item.doctor_user_id is not None else ""
                    print("innnnnnnnnnnnnnnnn")
                    item_dict = {
                        "case_id": case_item.case_id,
                        "doctor_user_id": doctor_user_id_val,
                        "patient_user_id": case_item.patient_user_id,
                        "status": case_item.status,
                        "insights": insights_value,
                        "created_at": case_item.created_at,
                        "image_path": image_path_item.image_path
                    }
                    item_dicts.append(item_dict)
                    break
        print("item_dicts: ", item_dicts)

        return item_dicts


casez = CRUDCase(Doctor)
