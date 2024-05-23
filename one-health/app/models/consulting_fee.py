from decimal import Decimal

from sqlalchemy import Column, String, func, ForeignKey, DECIMAL
import datetime

from app.db.base_class import Base
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from uuid import uuid4

class Consulting_Fee(Base):
    """
       Database Model for an application Doctor cases
       """
    __tablename__ = "Consulting_Fee"
    user_id = Column(CHAR(36), primary_key=True, index=True)
    fee = Column(DECIMAL(10, 2), index=True)
    commission = Column(DECIMAL(5, 2), index=True)
    user_type = Column(String(20), index=True)
    signature = Column(String(100))
    seal_stamp = Column(String(100))
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    created_by = Column(CHAR(36), index=True)
    updated_by = Column(CHAR(36), index=True)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "fee": float(self.fee) if isinstance(self.fee, Decimal) else self.fee,
            "commission": self.commission,
            "user_type": self.user_type,
            "created_by": self.created_by,
            "signature": self.signature,
            "seal_stamp": self.seal_stamp,
            "updated_by": self.updated_by
        }