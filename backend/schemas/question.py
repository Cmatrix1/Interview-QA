from pydantic import BaseModel

class Tag(BaseModel):
    ...

class Reference(BaseModel):
    ...

class DetailQuestion(BaseModel):
    id: int
    question_text: str
    answer: str
    level: str
    tags: list[str] = []
    references: list[str] = []
    
    next_question_id: int | None = None
    prev_question_id: int | None = None


class CreateQuestion(BaseModel):
    question_text: str
    answer: str
    level: str
    tags: list[str] = []
    references: list[str] = []


class UpdateQuestion(BaseModel):
    id: int 
    question_text: str
    answer: str
    level: str
    tags: list[str] = []
    references: list[str] = []