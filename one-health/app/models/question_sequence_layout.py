from pydantic import BaseModel


class QuestionSequenceLayout(BaseModel):
    KC1: str = None
    KC2: str = None
    KC3: str = None
    KC4: str = None
    KC5: str = None
    KC6: str = None
    KC7: str = None
    KC8: str = None
    KC9: str = None
    KC10: str = None
    question_sequence_Array: list[dict[str, int]]