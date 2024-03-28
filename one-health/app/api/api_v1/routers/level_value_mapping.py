from fastapi import APIRouter, HTTPException
from app.models.level_value_mapping import LevelValueMapping
from app.database.engine import mycursor, mydb
from typing import List

from starlette.responses import JSONResponse

router = APIRouter(prefix="/level_value_mapping", tags=["questions"])

@router.post("/add_key_criteria/")
def add_key_criteria(mapping: LevelValueMapping):
    level_id = mapping.level_id
    level_type = mapping.level_type
    
    # Insert each allowed value as a separate record
    for allowed_value in mapping.allowed_values:
        sql = "INSERT INTO level_value_mapping (level_id, level_type, allowed_value) VALUES (%s, %s, %s)"
        val = (level_id, level_type, allowed_value)
        mycursor.execute(sql, val)
        mydb.commit()
    
    #return {"message": "Key criteria added successfully"}
    return JSONResponse(content={"message": "Key criteria added successfully", "status": 200}, status_code=200)

@router.get("/view_key_criteria/")
def view_key_criteria():
    # Fetch all key criteria
    mycursor.execute("SELECT * FROM level_value_mapping")
    result = mycursor.fetchall()
    print("cdcewew, ", result)
    if not result:
        raise HTTPException(status_code=404, detail="No key criteria found")

    # Create a dictionary to store grouped elements
    grouped_data = {}

    # Iterate over the list and group elements
    for item in result:
        key = (item[0], item[1])  # Create a key based on first and second indices
        if key in grouped_data:
            # Concatenate third index value to existing value
            grouped_data[key] += f", {item[2]}"
        else:
            grouped_data[key] = item[2]  # Store third index value

    # Convert dictionary items to list of tuples
    grouped_list = [(key[0], key[1], value) for key, value in grouped_data.items()]

    #return {"key_criteria": result}
    return JSONResponse(content={"key_criteria": grouped_list, "status": 200}, status_code=200)

@router.put("/update_key_criteria/{level_id}")
def update_key_criteria(level_id: str, mapping: LevelValueMapping):
    # Delete existing key criteria for the given level_id
    delete_sql = "DELETE FROM level_value_mapping WHERE level_id = %s"
    delete_val = (level_id,)
    mycursor.execute(delete_sql, delete_val)
    mydb.commit()
    
    # Insert new key criteria
    insert_sql = "INSERT INTO level_value_mapping (level_id, level_type, allowed_value) VALUES (%s, %s, %s)"
    for allowed_value in mapping.allowed_values:
        insert_val = (level_id, mapping.level_type, allowed_value)
        mycursor.execute(insert_sql, insert_val)
        mydb.commit()

    #return {"message": f"Key criteria with ID {level_id} updated successfully"}
    return JSONResponse(content={"message": f"Key criteria with ID {level_id} updated successfully", "status": 200}, status_code=200)

@router.delete("/delete_key_criteria/{level_id}")
def delete_key_criteria(level_id: str):
    sql = "DELETE FROM level_value_mapping WHERE level_id = %s"
    val = (level_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    try:
        if mycursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Key criteria not found")
        # return {"message": f"Key criteria with ID {level_id} deleted successfully"}
        return JSONResponse(content={"message": f"Key criteria with ID {level_id} deleted successfully", "status": 200},
                            status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e.detail), "status": e.status_code}, status_code=e.status_code)

