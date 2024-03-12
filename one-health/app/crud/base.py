from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.db.base import Base
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel
from sqlalchemy.orm import Session, aliased, joinedload
from sqlalchemy import or_, literal, not_, select, Column, String
from app.models import User, Doctor

# Define custom types for SQLAlchemy models, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """Base class that can be extend by other action classes.
           Provides basic CRUD and listing operations.

        :param model: The SQLAlchemy models
        :type model: Type[ModelType]
        """
        self.model = model

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get(self, db: Session, id: str) -> Optional[ModelType]:
        print("fwfewfwe: ", id)
        print("dwqdfewfew: ", db.query(self.model).filter(or_(self.model.user_id == id)).first())
        return db.query(self.model).filter(or_(self.model.user_id == id)).first()

    # def get(self, db: Session, id: UUID4) -> Optional[ModelType]:
    #     return db.query(self.model).filter(self.model.user_id == id).first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID4) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    # def get_items(self, db: Session, skip: int = 0, limit: int = 10) -> ModelType:
    #     """
    #     Retrieve paginated items from the database.
    #
    #     :param db: SQLAlchemy database session
    #     :param skip: Number of items to skip
    #     :param limit: Maximum number of items to return per page
    #     :return: List of paginated items
    #     """
    #     print("fdsf: ", type(db.query(self.model).offset(skip).limit(limit).all()))
    #     return db.query(self.model).offset(skip).limit(limit).all()

    def get_items(self, db: Session,status: int,  skip: int = 0, limit: int = 10) -> List[Dict]:
        """
        Retrieve paginated items from the database.

        :param db: SQLAlchemy database session
        :param skip: Number of items to skip
        :param limit: Maximum number of items to return per page
        :return: List of paginated items
        """
        if status == 0:
            query = db.query(User).outerjoin(Doctor, User.user_id == Doctor.patient_user_id).filter(User.user_type == "Patient")

            # Filter the results to include only those users not present in the Doctor table
            query = query.filter(or_(Doctor.patient_user_id == None, literal(False)))

            query = query.offset(skip).limit(limit)
            items = query.all()
        elif status == 1:
            # query = db.query(User).join(Doctor, User.user_id == Doctor.patient_user_id).filter(User.user_type == "Patient")
            # # Apply offset and limit for pagination
            # query = query.offset(skip).limit(limit)

            query = (
                db.query(User, Doctor.doctor_user_id, Doctor.status)
                .join(Doctor, User.user_id == Doctor.patient_user_id)
                .filter(User.user_type == "Patient")
                .offset(skip)
                .limit(limit)
            )

            # Execute the query and fetch the results
            items = query.all()
            item_dicts = [
                {
                    "user_id": user.user_id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    # Add more fields as needed
                    "doctor_user_id": doctor_user_id,
                    "status": status
                }
                for user, doctor_user_id, status in items
            ]
            return item_dicts
        else:
            items = db.query(self.model).filter(User.user_type == "Patient").offset(skip).limit(limit).all()

        # Convert each item to a dictionary representation
        item_dicts = [item.__dict__ for item in items]
        return item_dicts
