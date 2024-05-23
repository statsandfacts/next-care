from sqlalchemy import Column, String, Date, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import CHAR, TIMESTAMP


class PromoCode(Base):
    __tablename__ = 'Promo_Code'

    Promo_Code = Column(String(50), primary_key=True)
    Discount = Column(DECIMAL(5, 2), nullable=True)
    Start_Date = Column(Date, nullable=True)
    End_Date = Column(Date, nullable=True)
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
            'Promo_Code': self.Promo_Code,
            'Discount': self.Discount,
            'Start_Date': self.Start_Date.strftime("%d-%m-%Y"),
            'created_at': self.created_at.strftime("%d-%m-%Y"),
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }
