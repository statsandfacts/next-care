from pydantic import BaseModel

class QuestionValueModel(BaseModel):
    value_id: int
    question_id: int
    allowed_values: list[str]

class QuestionValue(BaseModel):
    allowed_values: list[str]