from pydantic import BaseModel
from typing import Optional

class TaxBase(BaseModel):
    Tax: Optional[float] = None

class TaxCreate(TaxBase):
    Service_Type: str

class TaxUpdate(TaxBase):
    Service_Type: str
    pass

class TaxInDBBase(TaxBase):
    Service_Type: str

    class Config:
        orm_mode = True

class Tax(TaxInDBBase):
    pass
