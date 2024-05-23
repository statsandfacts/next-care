from decimal import Decimal

from sqlalchemy import Column, String, DECIMAL
from app.db.base_class import Base

class Tax(Base):
    __tablename__ = "Tax"
    Service_Type = Column(String(50), primary_key=True, index=True)
    Tax = Column(DECIMAL(5, 2), nullable=True)

    def to_dict(self):
        return {
            'Service_Type': self.Service_Type,
            'Tax': float(self.Tax) if isinstance(self.Tax, Decimal) else self.Tax
        }

