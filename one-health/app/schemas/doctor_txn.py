from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel

class DoctorTransactionRequest(BaseModel):
    order_id: Optional[int] = None
    case_id: str
    amount: str
    paid_type: str
    created_by: str
    updated_by: Optional[str] = None


class DoctorTransactionResponse(DoctorTransactionRequest):
    pass

class UpdateDoctorTransactionRequest(DoctorTransactionRequest):
    order_id: str

class DoctorTransaction(BaseModel):
    order_id: Union[str, None] = None
    case_id: Union[str, None] = None
    amount: Union[str, None] = None
    created_by: Union[str, None] = None
    paid_type: Union[str, None] = None
    updated_by: Union[datetime, None] = None
    created_at: Union[datetime, None] = None


class PaginationDoctorTxns(BaseModel):
    total: int
    items: List[DoctorTransaction]
    skip: int
    limit: int



