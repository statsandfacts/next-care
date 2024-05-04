import logging
import uuid
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.user_role import UserRole
from app.schemas.user import UserCreate, UserUpdate
from pydantic.types import UUID4
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core import security

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(User.email_id == email).first()

    def get_by_email_or_phone(self, db: Session, *, email: str, phone_number: str) -> Optional[User]:
        return db.query(self.model).filter(or_(User.email_id == email, User.phone_number == phone_number)).first()

    def get_by_user_id(self, db: Session, *, user_id: str) -> Optional[User]:
        return db.query(self.model).filter(User.user_id == user_id).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # db_obj = User(
        #     email=obj_in.email,
        #     hashed_password=get_password_hash(obj_in.password),
        #     full_name=obj_in.full_name,
        #     account_id=obj_in.account_id,
        # )

        try:
            db_obj = User()
            db_obj.government_id = obj_in.government_id
            db_obj.email_id = obj_in.email_id
            db_obj.user_type = obj_in.user_type
            # if obj_in.user_type == "patient":
            #     db_obj.user_type = "patient"
            # elif obj_in.user_type == "doctor":
            #     db_obj.user_type = "doctor"
            # else:
            #     db_obj.user_type = "admin"
            db_obj.government_idtype = obj_in.government_idtype
            db_obj.address = obj_in.address
            db_obj.last_name = obj_in.last_name
            db_obj.first_name = obj_in.first_name
            db_obj.qualification = obj_in.qualification
            db_obj.password = get_password_hash(obj_in.password)
            db_obj.specialization = obj_in.specialization
            db_obj.phone_number = obj_in.phone_number
            db_obj.govt_id_image = obj_in.govt_id_image
            db_obj.state = obj_in.state
            db_obj.zipcode = obj_in.zipcode
            db_obj.city = obj_in.city
            db_obj.gender = obj_in.gender
            db_obj.dob = obj_in.dob

            user_role = UserRole()
            user_role.user_id = db_obj.user_id
            user_role.role_id = self.assign_roles(db_obj)
            db_obj.user_type = user_role.role_id
            db_obj.user_role = user_role

            db.add(db_obj)
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
            logger.error("Error creating user", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Error creating user...",
            )

        return db_obj

    def assign_roles(self, db_obj):
        if db_obj.user_type.casefold() == "patient":
            return "1"
        elif db_obj.user_type.casefold() == "doctor":
            return "2"
        else:
            return "3"

    def update(
            self,
            db: Session,
            *,
            db_obj: User,
            obj_in: Union[UserUpdate, Dict[str, Any]],
    ) -> User:
        updated_user = None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        #print("fewfewvrew: ", len(obj_in.password))

        if len(obj_in.password) > 0:
            if "new_password" in update_data and not update_data["new_password"]:
                raise HTTPException(
                    status_code=409,
                    detail="Changing password requires new_password field",
                )

            if security.verify_password(update_data["password"], db_obj.password) is False:
                raise HTTPException(
                    status_code=409,
                    detail="Old password does not match",
                )
            hashed_password = get_password_hash(update_data["new_password"])
            del update_data["password"]
            update_data["password"] = hashed_password

        else:
            update_data["password"] = db_obj.password


        # if len(obj_in.password) > 0 and "password" in update_data:
        #     hashed_password = get_password_hash(update_data["password"])
        #     del update_data["password"]
        #     update_data["password"] = hashed_password
        # if len(obj_in.password) == 0:
        #     update_data["password"] = db_obj.password

        try:
            updated_user = super().update(db, db_obj=db_obj, obj_in=update_data)
        except IntegrityError as ie:
            logger.error("DB error occured", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=str(ie.orig),
            )
        return updated_user

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100,
    ) -> List[User]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def authenticate(
            self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def get_by_account_id(
            self,
            db: Session,
            *,
            account_id: UUID4,
            skip: int = 0,
            limit: int = 100,
    ) -> List[User]:
        return (
            db.query(self.model)
            .filter(User.account_id == account_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


def get_items(self, db: Session, skip: int = 0, limit: int = 10) -> User:
    """
    Retrieve paginated items from the database.

    :param db: SQLAlchemy database session
    :param skip: Number of items to skip
    :param limit: Maximum number of items to return per page
    :return: List of paginated items
    """
    return db.query(self.model).offset(skip).limit(limit).all()


user = CRUDUser(User)
