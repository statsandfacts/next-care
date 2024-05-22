import logging
from sqlalchemy.orm import Session
from app.schemas.user import CaseCreate, CaseUpdate, PatientDashboardResponse, PatientDashboardResponseList, ImagePath, \
    CaseReport, CaseReportResponse, DiagnosisMedicine, DiagnosisMedicineReport, PaginatedItemDoctorList
from app.models.doctor_transaction import Doctor_Transaction
from app.models.doctor import Doctor
from app.models.user_upload import UserUpload
from app.models.user_session import UserSession
from sqlalchemy.exc import IntegrityError
from app.crud.base import CRUDBase
from fastapi import HTTPException
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import or_, func, and_, asc, desc
from app.models.user import User
from app.schemas.doctor_txn import DoctorTransactionRequest, DoctorTransactionResponse, UpdateDoctorTransactionRequest, PaginationDoctorTxns
from starlette.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CRUDDoctorTransaction(CRUDBase[Doctor_Transaction, DoctorTransactionRequest, DoctorTransactionResponse]):

    def create_doctor_transaction(self, db: Session, obj_in: DoctorTransactionRequest) -> Doctor_Transaction:
        try:
            print("obj_in: ", obj_in.order_id)
            db_trasaction = db.query(Doctor_Transaction).filter(Doctor_Transaction.order_id == obj_in.order_id).first()
            print("db_trasaction: ", db_trasaction)
            print("type:" , type(db_trasaction))
            if not db_trasaction:
                logger.info("Creating new doctor transaction")
                db_case = db.query(Doctor).filter(Doctor.case_id == obj_in.case_id).first()
                if not db_case:
                    return JSONResponse(content={"detail": "case doesn't exist for the transaction you trying to create",
                                                 "status": "409"}, status_code=409)
                if db_case.status != "Approved":
                    return JSONResponse(
                        content={"detail": "case has not been approved yet", "status": "409"}, status_code=409)
                print("defwefgefgEWL: ", db_case.doctor_user_id)
                new_transaction = Doctor_Transaction()
                new_transaction.case_id = db_case.case_id
                new_transaction.user_id = db_case.doctor_user_id
                new_transaction.amount = obj_in.amount
                new_transaction.paid_type = obj_in.paid_type
                new_transaction.created_by = obj_in.created_by
                new_transaction.updated_by = obj_in.updated_by
                #new_transaction.doctor = db_case
                db.add(new_transaction)
                db.commit()
                db.refresh(new_transaction)
                logger.info("Created doctor transaction")
                return JSONResponse(
                    content={"detail": "Doctor transaction has been successfully created", "status": "200"}, status_code=200)
            else:
                logger.info("Updating doctor transaction")
                self.update_doctor_transaction(db, db_obj=db_trasaction, obj_in=obj_in)
                return JSONResponse(
                    content={"detail": "Doctor transaction has been successfully updated", "status": "200"},
                    status_code=200)
        except IntegrityError as ie:
            logger.error("DB error occured", exc_info=True)
            return JSONResponse(content={"detail": str(ie.detail), "status": ie.status_code}, status_code=ie.status_code)
        except Exception as e:
            logger.error("DB error occured", exc_info=True)
            return JSONResponse(content={"detail": "DB error occured while creating or updating the record.", "status": 500},
                                status_code=500)

    def update_doctor_transaction(
            self,
            db: Session,
            *,
            db_obj: Doctor_Transaction,
            obj_in: Union[DoctorTransactionRequest, Dict[str, Any]],
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
        logger.info("Updated doctor transaction")
        return updated_case

    def get_doc_txn_per_id(self, db: Session, user_id: str, skip: int = 0, limit: int = 10, order_by_field: str = 'updated_at',
                           order_by_direction: str = 'asc'):
        # Validate order_by_direction to ensure it's either 'asc' or 'desc'
        print("order_by_field: ", order_by_field)
        print("order_by_direction: ", order_by_direction)
        if order_by_direction not in ['asc', 'desc']:
            return JSONResponse(
                content={"detail": "order_by_direction must be either 'asc' or 'desc'", "status": 400},
                status_code=400)
        if not order_by_field:
            order_by_field = 'updated_at'
        # Dynamically construct the order_by expression
        order_by_exp = asc(getattr(Doctor_Transaction, order_by_field)) if order_by_direction == 'asc' else desc(
            getattr(Doctor_Transaction, order_by_field))

        query = db.query(Doctor_Transaction).filter(Doctor_Transaction.user_id == user_id).order_by(order_by_exp)
        total_len = query.count()
        doc_txns = query.offset(skip).limit(limit).all()
        item_dicts = [item.__dict__ for item in doc_txns]
        return PaginationDoctorTxns(
            total=total_len,
            items=item_dicts,
            skip=skip,
            limit=limit,
        )

    def get_doc_txn_per_case(self, db: Session, case_id: str, skip: int = 0, limit: int = 10, order_by_field: str = 'updated_at',
                           order_by_direction: str = 'asc'):
        # Validate order_by_direction to ensure it's either 'asc' or 'desc'
        if order_by_direction not in ['asc', 'desc']:
            return JSONResponse(
                content={"detail": "order_by_direction must be either 'asc' or 'desc'", "status": 400},
                status_code=400)
        if not order_by_field:
            order_by_field = 'updated_at'
        # Dynamically construct the order_by expression
        order_by_exp = asc(getattr(Doctor_Transaction, order_by_field)) if order_by_direction == 'asc' else desc(
            getattr(Doctor_Transaction, order_by_field))

        query = db.query(Doctor_Transaction).filter(Doctor_Transaction.case_id == case_id).order_by(order_by_exp)
        total_len = query.count()
        doc_txns = query.offset(skip).limit(limit).all()
        item_dicts = [item.__dict__ for item in doc_txns]
        return PaginationDoctorTxns(
            total=total_len,
            items=item_dicts,
            skip=skip,
            limit=limit,
        )


doctor_transaction = CRUDDoctorTransaction(Doctor_Transaction)
