from db.models.question import Question
from sqlalchemy import func
from sqlalchemy.orm import Session
from db.models.tag import Tag
from db.models.refrence import Reference
from schemas.question import DetailQuestion
from utils.exceptions.questions import QuestionNotFoundException


def question_exist(question_id: int, db: Session) -> bool:
    question = db.query(Question.id).filter(Question.id == question_id).scalar()
    return bool(question)


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
    raise QuestionNotFoundException(f"Question with ID {id} not found")


def create_question(question_text: str, answer: str, level: str, tags: list[Tag], references: list[Reference], db: Session):
    question_object = Question(
        question_text=question_text,
        answer=answer,
        level=level
    )
    question_object.tags.extend(tags)
    question_object.references.extend(references)
    db.add(question_object)
    db.commit()
    return question_object


def update_question(question_id: int, question_text: str, answer: str, level: str, tags: list[Tag], references: list[Reference], db: Session):
    question_object = db.query(Question).filter(Question.id == question_id).first()
    if not question_object:
        raise QuestionNotFoundException(f"Question with ID {question_id} not found")

    question_object.question_text = question_text
    question_object.answer = answer
    question_object.level = level

    question_object.tags.clear()
    question_object.references.clear()

    question_object.tags.extend(tags)
    question_object.references.extend(references)

    db.commit()
    return question_object
