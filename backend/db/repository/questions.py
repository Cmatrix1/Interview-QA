from db.models.question import Question
# from schemas.question import
from sqlalchemy import func
from sqlalchemy.orm import Session
from schemas.question import DetailQuestion


def list_questions(db: Session) -> list[Question]:
    questions = db.query(
        Question.id,
        Question.question_text,
        Question.level,
    ).order_by(
        Question.id
    ).all()
    return questions


def detail_questions(id: int, db: Session) -> DetailQuestion:
    next_question_subquery = db.query(Question.id).order_by(
        Question.id).filter(Question.id > id).limit(1).scalar()
    prev_question_subquery = db.query(Question.id).order_by(
        Question.id.desc()).filter(Question.id < id).limit(1).scalar()

    question, next_question, prev_question = db.query(
        Question, next_question_subquery, prev_question_subquery
    ).filter(Question.id == id).first()

    if question:
        return DetailQuestion(
            **question.as_dict(),
            next_question_id=next_question,
            prev_question_id=prev_question
            )
    return None
