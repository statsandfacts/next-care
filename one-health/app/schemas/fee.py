from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel

class CreateFeeRequest(BaseModel):
    user_id: str
    fee: str
    commission: str
    user_type: str
    created_by: str
    updated_by: str
    seal_stamp: str
    signature: str

class UpdateFeeRequest(CreateFeeRequest):
    pass

class UpdatePromoCodeRequest(BaseModel):
    Promo_Code: str
    Discount: str
    Start_Date: str
    End_Date: str
    created_by: str
    updated_by: str



