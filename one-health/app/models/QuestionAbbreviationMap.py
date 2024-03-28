from typing import Optional

from pydantic import BaseModel


class QuestionAbbreviationMap(BaseModel):
    question_id: int
    question: str
    answer: str
    abbreviation: Optional[str] = None