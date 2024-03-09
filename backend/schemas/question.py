from pydantic import BaseModel
from typing import List

class Tag(BaseModel):
    ...

class Reference(BaseModel):
    ...

class DetailQuestion(BaseModel):
    id: int
    question_text: str
    answer: str
    level: str
    tags: List[Tag] = []
    references: List[Reference] = []
    
    next_question_id: int | None = None
    prev_question_id: int | None = None


class CreateQuestion(BaseModel):
    id: int
    question_text: str
    answer: str
    level: str
    tags: List[Tag] = []
    references: List[Reference] = []

