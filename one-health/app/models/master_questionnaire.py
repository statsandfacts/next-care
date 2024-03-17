from pydantic import BaseModel

class MasterQuestionnaireModel(BaseModel):
    question_id: int
    question_type: str
    description: str
    multiple_selection_allowed: bool

class MasterQuestionnaireCreate(BaseModel):
    question_type: str
    description: str
    multiple_selection_allowed: bool