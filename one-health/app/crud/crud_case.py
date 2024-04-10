import logging

from sqlalchemy.orm import Session
from app.schemas.user import CaseCreate, CaseUpdate, PatientDashboardResponse, PatientDashboardResponseList, ImagePath, \
    CaseReport, CaseReportResponse, DiagnosisMedicine, DiagnosisMedicineReport
from app.models.doctor import Doctor
from app.models.user_upload import UserUpload
from app.models.user_session import UserSession
from sqlalchemy.exc import IntegrityError
from app.crud.base import CRUDBase
from fastapi import HTTPException
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import or_, func, and_
from app.models.user import User
from app.models.diagnosis_medicine_mapping import DiagnosisMedicineMapping

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
            # db_obj.doctor_user_id = obj_in.doctor_user_id
            db_obj.patient_user_id = obj_in.patient_id
            db_obj.status = 'In Progress'

            # model call
            upload_obj = UserUpload()
            upload_obj.user_id = obj_in.patient_id
            upload_obj.image_path = obj_in.image_path
            upload_obj.image_output_label = "Acne grade 1"  # model_output
            db_obj.user_uploads = upload_obj

            db.add(db_obj)
            # db.add(upload_obj)
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
            item_dicts = [{**item.__dict__, 'created_date': item.created_at.strftime("%B %d, %Y")} for item in case_items]

            return item_dicts
        elif not doctor_user_id and status:
            case_items = db.query(self.model).filter(or_(self.model.status == status)).all()
            print("elif case items", case_items)
        elif not status and doctor_user_id:
            case_items = db.query(self.model).filter(self.model.doctor_user_id == doctor_user_id).all()
            print("elif status null items", case_items)
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
                index = index + 1
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
                    print("created_at: ", case_item.created_at)
                    item_dict = {
                        "case_id": case_item.case_id,
                        "doctor_user_id": doctor_user_id_val,
                        "patient_user_id": case_item.patient_user_id,
                        "status": case_item.status,
                        "insights": insights_value,
                        "created_date": case_item.created_at.strftime("%B %d, %Y"),
                        "image_path": image_path_item.image_path,
                        "remarks": case_item.remarks,
                        "doctor_edit_image_insights": case_item.doctor_edit_image_insights
                    }
                    item_dicts.append(item_dict)
                    break
        print("item_dicts: ", item_dicts)

        return item_dicts

    def get_patient_dashboard(self, db: Session, db_obj: User):
        case_pages = []
        cases = db.query(self.model).filter(Doctor.patient_user_id == db_obj.user_id).all()
        if len(cases) > 0:
            for case in cases:
                upload_db = db.query(UserUpload).filter(
                    UserUpload.user_id == case.patient_user_id).first()
                diseases = upload_db.image_output_label
                doctor_obj = db.query(User).filter(User.user_id == case.doctor_user_id).first()
                print("doctor_obj: ", doctor_obj)
                doctor_name = ""
                if doctor_obj:
                    doctor_name = doctor_obj.first_name + " " + doctor_obj.last_name
                case_page = PatientDashboardResponse(
                    case_id=case.case_id,
                    diseases=diseases,
                    doctor_name=doctor_name,
                    created_date=case.created_at.strftime("%B %d, %Y"),
                    case_status= case.status
                )
                case_pages.append(case_page)
        return case_pages

    def get_case_report(self, db: Session, case_id: str):
        case = db.query(self.model).filter(self.model.case_id == case_id).first()
        if not case:
            raise HTTPException(
                status_code=404,
                detail="case doesn't exist in the system."
            )
        user_upload = db.query(UserUpload).filter(
            UserUpload.case_id == case.case_id).first()

        image_path_list = user_upload.image_path.split(',') # change single list logic here
        image_output_label_list = user_upload.image_output_label.split(',')
        mapped_values = [ImagePath(name=path, value=label) for path, label in
                         zip(image_path_list, image_output_label_list)]

        user_session = db.query(UserSession).filter(UserSession.user_id == case.patient_user_id).first()
        question_ans = [{}]
        if user_session.question_answers:
            question_ans = user_session.question_answers

        case_report = CaseReport(
            remarks= case.remarks,
            insights= case.insights,
            image_path=mapped_values,
            question_answers=question_ans
        )
        return case_report

    def get_prescription(self, db: Session, case_id):
        case = db.query(self.model).filter(self.model.case_id == case_id).first()
        if not case:
            raise HTTPException(
                status_code=404,
                detail="case doesn't exist in the system."
            )
        if not case.doctor_user_id:
            raise HTTPException(
                status_code=400,
                detail="Please assign the case to a doctor first"
            )
        visit = "First"
        if case.sec_case_id:
            visit = "Second"
        user_doc = db.query(User).filter(User.user_id == case.doctor_user_id).first()
        doctor_name = user_doc.first_name + " " + user_doc.last_name
        user_upload = db.query(UserUpload).filter(
            UserUpload.case_id == case.case_id).first()
        image_output_label_list = user_upload.image_output_label.split(',')
        diagnosis_list = db.query(DiagnosisMedicineMapping).filter(
            DiagnosisMedicineMapping.diagnosis.in_(image_output_label_list),
            DiagnosisMedicineMapping.visit == visit
        ).all()
        diagnose_response_list = []
        for item in diagnosis_list:
            diagnose = DiagnosisMedicine(diagnosis=item.diagnosis,
                                         medicine=item.medicine,
                                         dosage=item.dosage
                                         )
            diagnose_response_list.append(diagnose)
        return DiagnosisMedicineReport(patient_name= user_upload.user.first_name + " " + user_upload.user.last_name,
                                       doctor_name= doctor_name, date= case.updated_at.strftime("%B %d, %Y"),
                                       diagnosis_medicines=diagnose_response_list)


casez = CRUDCase(Doctor)
