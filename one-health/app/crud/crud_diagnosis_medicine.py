import logging
from app.schemas.user import SaveUserResponse
from app.models.diagnosis_medicine_mapping import DiagnosisMedicineMapping
from app.crud.base import CRUDBase
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user import CreateDiagnosis
from app.models.diagnose_code_table import DiagnoseCodeTable
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CRUDDiagnosisMedicine(CRUDBase[DiagnosisMedicineMapping, CreateDiagnosis, CreateDiagnosis]):

    def get_mapping(self, db: Session, mapping_id: str) -> Optional[DiagnosisMedicineMapping]:
        return db.query(DiagnosisMedicineMapping).filter(DiagnosisMedicineMapping.mapping_id == mapping_id).first()

    def get_mapping_by_visit_diagnosis(self, db: Session, visit: str, diagnosis: str):
        return db.query(DiagnosisMedicineMapping).filter(
            DiagnosisMedicineMapping.visit == visit,
            DiagnosisMedicineMapping.diagnosis == diagnosis
        ).first()

    def get_all_mappings(self, db: Session) -> List[DiagnosisMedicineMapping]:
        return db.query(DiagnosisMedicineMapping).all()

    def create_mapping(self, db: Session, visit: str, diagnosis: str, medicine: str, company: str,
                       dosage: str, is_active: str, doctor_user_id: str) -> DiagnosisMedicineMapping:
        try:
            if self.get_mapping_by_visit_diagnosis(db, visit=visit, diagnosis=diagnosis):
                return JSONResponse(
                    content={"mappings": "visit and diagnosis combination mapping already exist", "status": 400},
                    status_code=400)

            new_mapping = DiagnosisMedicineMapping(visit=visit, diagnosis=diagnosis, medicine=medicine, company=company,
                                                   dosage=dosage, is_active=is_active, doctor_user_id=doctor_user_id)
            db.add(new_mapping)
            db.commit()
            db.refresh(new_mapping)
            return JSONResponse(content={"message": "mapping created successfully", "status": 200}, status_code=200)
        except Exception:
            logger.error("Error while creating mapping record...")
            return JSONResponse(content={"detail": "Error while creating mapping", "status": 500}, status_code=500)

    def update_mapping(self, db: Session, mapping_id:str, visit: str, diagnosis: str, medicine: str, company: str,
                       dosage: str, is_active: str, doctor_user_id: str) -> DiagnosisMedicineMapping:
        mapping = db.query(DiagnosisMedicineMapping).filter(DiagnosisMedicineMapping.mapping_id == mapping_id).first()
        if not mapping:
            raise HTTPException(status_code=404, detail="Mapping not found")
        mapping.visit = visit
        mapping.diagnosis = diagnosis
        mapping.medicine = medicine
        mapping.company = company
        mapping.dosage = dosage
        mapping.is_active = is_active
        mapping.doctor_user_id = doctor_user_id
        db.commit()
        db.refresh(mapping)
        return mapping

    def delete_mapping(self, db: Session, mapping_id: str) -> None:
        mapping = db.query(DiagnosisMedicineMapping).filter(DiagnosisMedicineMapping.mapping_id == mapping_id).first()
        if not mapping:
            raise HTTPException(status_code=404, detail="Mapping not found")
        db.delete(mapping)
        db.commit()


    def get_all_diagnosis(self, db:Session) -> List[DiagnoseCodeTable]:
        return db.query(DiagnoseCodeTable).all()


diagnosis = CRUDDiagnosisMedicine(DiagnosisMedicineMapping)