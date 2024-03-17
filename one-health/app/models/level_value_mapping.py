from pydantic import BaseModel

class LevelValueMapping(BaseModel):
    level_id: str
    level_type: str
    allowed_values: list[str]