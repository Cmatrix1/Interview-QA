from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from db.repository.questions import question_exist


def validate_question_id(question_id: int, db: Session = Depends(get_db)):
    if question_exist(question_id=question_id, db=db):
        return question_id
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Question With ID '{question_id}' not found"
        )