from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session,sessionmaker
from typing import List
#from app.database.deps import SessionLocal
from app.crud.level_value_mapping import create_key_criteria,update_record_by_key,delete_record_by_key,get_all_records
from app.api import deps
from app.api.deps import get_db
from fastapi import Depends


from app.models.level_value_mapping import LevelValueMapping,LevelValueMappingDB
from starlette.responses import JSONResponse

router = APIRouter(prefix="/level_value_mapping", tags=["level_value_mapping"])

@router.post("/add_key_criteria/")
async def ingest_data(data: LevelValueMapping, db: Session = Depends(deps.get_db)):
    create_key_criteria(data, db)
    return JSONResponse(content={"message": "Data ingested successfully", "status": 200}, status_code=200)


@router.put("/update_key_criteria/{level_id}")
async def update_data(level_id: str, data: LevelValueMapping, db: Session = Depends(deps.get_db)):
    try:
        update_record_by_key(level_id, data.level_type, data.allowed_values, db)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update data: {str(e)}")
    return JSONResponse(content={"message": "Data updated successfully", "status": 200}, status_code=200)

@router.delete("/delete_key_criteria/{level_id}")
async def delete_data(level_id: str, db: Session = Depends(deps.get_db)):
    try:
        delete_record_by_key(level_id, db)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete data: {str(e)}")
    return JSONResponse(content={"message": "Data deleted successfully", "status": 200}, status_code=200)

@router.get("/view_key_criteria/")
async def get_all_data(db: Session = Depends(deps.get_db)):
    try:
        all_records = get_all_records(db)
        grouped_data = {}
        for item in all_records:
            key = (item.level_id, item.level_type)  # Access attributes by name
            if key in grouped_data:
                grouped_data[key] += f", {item.allowed_value}"
            else:
                grouped_data[key] = item.allowed_value

        # Convert dictionary items to list of tuples
        grouped_list = [(key[0], key[1], value) for key, value in grouped_data.items()]
        sorted_grouped_list = sorted(grouped_list, key=lambda x: x[0])

        return JSONResponse(content={"key_criteria": sorted_grouped_list, "status": 200}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve data: {str(e)}")
