from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app import schemas
from app.api.deps import get_db


@router.get("/items/", response_model=schemas.PaginatedItemList)
def get_items(
        db: Session = Depends(get_db),
        page: int = Query(default=1, ge=1),
        limit: int = Query(default=10, ge=1),
):
    # Calculate skip value based on page number and page size
    skip = (page - 1) * limit

    # Retrieve paginated items from the database
    items = crud.get_items(db, skip=skip, limit=limit)

    # Count total number of items in the database
    total_items = crud.count_items(db)

    # Return paginated items along with metadata
    return schemas.PaginatedItemList(
        total=total_items,
        items=items,
        skip=skip,
        limit=limit,
    )
