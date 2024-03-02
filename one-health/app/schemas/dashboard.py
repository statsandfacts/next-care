from typing import List

from pydantic.v1 import BaseModel

class CaseItems:
    user_first_name: str

class PaginatedItemList(BaseModel):
    total: int
    items: List[CaseItems]
    skip: int
    limit: int


