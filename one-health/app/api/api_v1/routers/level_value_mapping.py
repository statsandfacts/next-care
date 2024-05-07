from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session,sessionmaker
from typing import List
#from app.database.deps import SessionLocal
from app.crud.level_value_mapping import create_key_criteria,update_record_by_key,delete_record_by_key,get_all_records
from app.api import deps
from app.api.deps import get_db
from fastapi import Depends


from app.models.level_value_mapping import LevelValueMapping,LevelValueMappingDB

router = APIRouter(prefix="/level_value_mapping", tags=["level_value_mapping"])

@router.post("/add_key_criteria/")
async def ingest_data(data: LevelValueMapping, db: Session = Depends(deps.get_db)):
    create_key_criteria(data, db)
    return {"message": "Data ingested successfully"}


@router.put("/update_key_criteria/{level_id}")
async def update_data(level_id: str, data: LevelValueMapping, db: Session = Depends(deps.get_db)):
    try:
        update_record_by_key(level_id, data.level_type, data.allowed_values, db)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update data: {str(e)}")
    return {"message": "Data updated successfully"}

@router.delete("/delete_key_criteria/{level_id}")
async def delete_data(level_id: str, db: Session = Depends(deps.get_db)):
    try:
        delete_record_by_key(level_id, db)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete data: {str(e)}")
    return {"message": "Data deleted successfully"}

@router.get("/view_key_criteria/")
async def get_all_data(db: Session = Depends(deps.get_db)):
    try:
        all_records = get_all_records(db)
        return all_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve data: {str(e)}")