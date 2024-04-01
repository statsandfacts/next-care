import logging
from app.schemas.user import SaveUserResponse
from app.models.user_session import UserSession
from app.crud.base import CRUDBase
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional, Union
from sqlalchemy.exc import IntegrityError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CRUDSession(CRUDBase[UserSession, SaveUserResponse, SaveUserResponse]):

    def get_by_session_id(self, db: Session, *, session_id: str, user_id: str) -> Optional[UserSession]:
        return db.query(self.model).filter(UserSession.session_id == session_id, UserSession.user_id == user_id).first()

    def get_by_user_id(self, db: Session, *, user_id: str) -> Optional[UserSession]:
        return db.query(self.model).filter(UserSession.user_id == user_id).first()

    def createOrUpdateSession(self, db: Session, session_id: str, user_id: str):
        user_session = db.query(self.model).filter(UserSession.user_id == user_id).first()
        print("sambeet: ", user_session)
        if user_session is None:
            self.create_session(db, user_id=user_id, session_id=session_id)
        else:
            user_session_obj = SaveUserResponse(
                session_id=session_id,
                user_id=user_id,
                question_answers=[{"": ""}]
            )
            self.update_user_session(db, db_obj=user_session, obj_in=user_session_obj)

    def update_user_session(self, db: Session,
                            *,
                            db_obj: UserSession,
                            obj_in: Union[SaveUserResponse, Dict[str, Any]],
                            ) -> UserSession:
        updated_case = None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        try:
            print("userdsdfew seesion: ", update_data)
            updated_case = super().update(db, db_obj=db_obj, obj_in=update_data)
        except IntegrityError as ie:
            logger.error("DB error occured", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=str(ie.orig)
            )
        return updated_case

    def create_session(self, db: Session, *, user_id: str, session_id: str) -> UserSession:

        try:
            db_obj = UserSession()
            db_obj.user_id = user_id
            db_obj.session_id = session_id

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
            logger.error("Error creating the case", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Error creating case...",
            )

        return db_obj


user_session = CRUDSession(UserSession)
