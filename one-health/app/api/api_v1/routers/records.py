from fastapi import APIRouter, HTTPException
from app.models.question_sequence_layout import QuestionSequenceLayout
from app.database.engine import mycursor, mydb
from typing import List
import hashlib

router = APIRouter(prefix="/records", tags=["questions"])

@router.post("/create_records/")
async def create_records(QuestionSequenceLayoutList: List[QuestionSequenceLayout]):
    for QuestionSequenceLayout in QuestionSequenceLayoutList:
        kc_values = [getattr(QuestionSequenceLayout, f"KC{i}", None) for i in range(1, 11)]
        kc_columns = [f"KC{i}" for i in range(1, 11) if getattr(QuestionSequenceLayout, f"KC{i}", None) is not None]
        
        # Extract question IDs and sequences from the request
        question_sequence_array = QuestionSequenceLayout.question_sequence_Array
        
        # Validate request data
        if len(question_sequence_array) == 0:
            raise HTTPException(status_code=400, detail="At least one question-sequence pair must be provided")
        
        for item in question_sequence_array:
            if "question_id" not in item or "sequence_id" not in item:
                raise HTTPException(status_code=400, detail="Each item in question_sequence_Array must have question_id and sequence_id")
            
            question_id = item["question_id"]
            sequence_id = item["sequence_id"]
            
            # Calculate hexcode based on combinations of KC1 to KC10
            key_combination = hashlib.md5(''.join(filter(None, kc_values)).encode()).hexdigest()
            
            # Build SQL query and values
            sql = f"INSERT INTO Question_sequence_layout ({', '.join(kc_columns)}, question_id, sequence, KEY_COMBINATION) VALUES ({', '.join(['%s'] * len(kc_columns))}, %s, %s, %s)"
            val = tuple(filter(None, kc_values)) + (question_id, sequence_id, key_combination)
            
            # Execute SQL query
            mycursor.execute(sql, val)
            mydb.commit()
    
    return {"message": "Records created successfully"}

# Update records endpoint
@router.put("/update_records/{key_combination}")
async def update_records(key_combination: str, QuestionSequenceLayout: QuestionSequenceLayout):
    kc_values = [getattr(QuestionSequenceLayout, f"KC{i}", None) for i in range(1, 11)]
    kc_columns = [f"KC{i}=%s" for i in range(1, 11) if getattr(QuestionSequenceLayout, f"KC{i}", None) is not None]
    
    if not kc_columns:
        raise HTTPException(status_code=400, detail="At least one KC column must be provided")
    
    sql = f"UPDATE Question_sequence_layout SET {', '.join(kc_columns)} WHERE KEY_COMBINATION = %s"
    val = [v for v in kc_values if v is not None] + [key_combination]
    
    mycursor.execute(sql, val)
    mydb.commit()
    
    # Update question_sequence_Array if provided
    if QuestionSequenceLayout.question_sequence_Array:
        for item in QuestionSequenceLayout.question_sequence_Array:
            question_id = item["question_id"]
            sequence_id = item["sequence_id"]
            
            # Update SQL query and values
            sql = "UPDATE Question_sequence_layout SET sequence = %s WHERE question_id = %s AND KEY_COMBINATION = %s"
            val = (sequence_id, question_id, key_combination)
            
            mycursor.execute(sql, val)
            mydb.commit()
    
    return {"message": f"Records with key_combination '{key_combination}' updated successfully"}

# Delete records endpoint
@router.delete("/delete_records/{key_combination}")
async def delete_records(key_combination: str):
    sql = "DELETE FROM Question_sequence_layout WHERE KEY_COMBINATION = %s"
    val = (key_combination,)
    
    mycursor.execute(sql, val)
    mydb.commit()
    
    return {"message": f"Records with key_combination '{key_combination}' deleted successfully"}

# Show records endpoint based on key_combination
@router.get("/show_records/{key_combination}")
async def show_records(key_combination: str):
    sql = "SELECT * FROM your_table WHERE KEY_COMBINATION = %s"
    val = (key_combination,)
    
    mycursor.execute(sql, val)
    records = mycursor.fetchall()
    
    if not records:
        raise HTTPException(status_code=404, detail=f"No records found with key_combination '{key_combination}'")
    
    return records
