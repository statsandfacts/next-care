from fastapi import APIRouter
from app.models.master_questionnaire import MasterQuestionnaireCreate, MasterQuestionnaireModel, MasterQuestionnareDetail
from app.models.question_value import QuestionValueModel,QuestionValue
from app.database.engine import mycursor, mydb
from fastapi import HTTPException
from typing import List

router = APIRouter(prefix="/master_questionnaire", tags=["questions"])

@router.post("/add_questionnaire/")
def add_questionnaire(master_questionnaire: MasterQuestionnaireCreate, question_values: List[QuestionValue]):
    # Insert master questionnaire
    sql = "INSERT INTO master_questionnaire (question_type, description, multiple_selection_allowed) VALUES (%s, %s, %s)"
    val = (master_questionnaire.question_type, master_questionnaire.description, master_questionnaire.multiple_selection_allowed)
    mycursor.execute(sql, val)
    mydb.commit()
    
    question_id = mycursor.lastrowid
    
    # Insert question values
    for qv in question_values:
        sql = "INSERT INTO question_values (question_id, allowed_values) VALUES (%s, %s)"
        val = (question_id, ','.join(qv.allowed_values))
        mycursor.execute(sql, val)
        mydb.commit()

    return {"message": "Questionnaire added successfully"}

@router.get("/get_questionnaires/")
def get_questionnaires():
    # Fetch all master questionnaires
    mycursor.execute("SELECT * FROM master_questionnaire")
    master_questionnaires_data = mycursor.fetchall()
    
    questionnaires = []
    for mq_data in master_questionnaires_data:
        master_questionnaire = MasterQuestionnaireModel(question_id=mq_data[0], question_type=mq_data[1], description=mq_data[2], multiple_selection_allowed=bool(mq_data[3]))
        
        # Fetch question values for each master questionnaire
        mycursor.execute("SELECT * FROM question_values WHERE question_id = %s", (mq_data[0],))
        question_values_data = mycursor.fetchall()
        
        question_values = []
        for qv_data in question_values_data:
            question_values.append(QuestionValueModel(question_id=qv_data[0], value_id=qv_data[1], allowed_values=qv_data[2].split(',')))
        
        questionnaires.append({"master_questionnaire": master_questionnaire.dict(), "question_values": [qv.dict() for qv in question_values]})
    
    return questionnaires


@router.put("/update_questionnaire/{question_id}")
def update_questionnaire(question_id: int, master_questionnaire: MasterQuestionnaireCreate, question_values: List[QuestionValue]):
    # Check if question ID exists
    mycursor.execute("SELECT COUNT(*) FROM master_questionnaire WHERE question_id = %s", (question_id,))
    result = mycursor.fetchone()
    if result[0] == 0:
        raise HTTPException(status_code=404, detail="Questionnaire not found")

    # Update master questionnaire
    sql = "UPDATE master_questionnaire SET question_type = %s, description = %s, multiple_selection_allowed = %s WHERE question_id = %s"
    val = (master_questionnaire.question_type, master_questionnaire.description, master_questionnaire.multiple_selection_allowed, question_id)
    mycursor.execute(sql, val)
    mydb.commit()
    
    # Delete existing question values
    sql = "DELETE FROM question_values WHERE question_id = %s"
    val = (question_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    
    # Insert updated question values
    for qv in question_values:
        sql = "INSERT INTO question_values (question_id, allowed_values) VALUES (%s, %s)"
        val = (question_id, ','.join(qv.allowed_values))
        mycursor.execute(sql, val)
        mydb.commit()

    return {"message": f"Questionnaire with ID {question_id} updated successfully"}

@router.delete("/delete_questionnaire/{question_id}")
def delete_questionnaire(question_id: int):
    # Delete master questionnaire
    sql = "DELETE FROM master_questionnaire WHERE question_id = %s"
    val = (question_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    
    # Delete question values
    sql = "DELETE FROM question_values WHERE question_id = %s"
    val = (question_id,)
    mycursor.execute(sql, val)
    mydb.commit()

    return {"message": f"Questionnaire with ID {question_id} deleted successfully"}


@router.post("/show_question_details")
def show_question_details(master_questionnaire: MasterQuestionnareDetail):
    question_details = []
    for question_id in master_questionnaire.question_ids:
        try:
            # Fetch question details
            mycursor.execute("SELECT question_id, question_type FROM master_questionnaire WHERE question_id = %s", (question_id,))
            question_data = mycursor.fetchone()

            if question_data:
                question_type = question_data[1]

                # Fetch allowed values
                mycursor.execute("SELECT allowed_values FROM question_values WHERE question_id = %s", (question_id,))
                allowed_values_data = mycursor.fetchone()
                allowed_values = allowed_values_data[0].split(',') if allowed_values_data else []

                question_details.append({
                    "question_id": question_data[0],
                    "question_type": question_type,
                    "allowed_values": allowed_values
                })
            else:
                question_details.append({
                    "question_id": question_id,
                    "question_type": None,  # or any default value
                    "allowed_values": []    # or any default value
                })
        except Exception as e:
            # Log the exception if necessary
            print(f"Error processing question ID {question_id}: {e}")

    return question_details
