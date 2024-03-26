from schemas.question import CreateQuestion, UpdateQuestion
from db.repository import tags, refrence, questions
from db.models.question import Question
from sqlalchemy.orm import Session


def handle_tags(tag_list: list[str], db: Session):
    existing_tags = tags.get_mulitiple_tags(tag_list, db=db)
    existing_tags_names = set(tag.name for tag in existing_tags)
    not_existing_tags = set(tag_list) - existing_tags_names
    if not_existing_tags:
        new_tags = tags.create_mulitiple_tags(not_existing_tags, db=db)
        existing_tags.append(new_tags)

    return existing_tags


def handle_question_reference(reference_list: list[str], db: Session):
    existing_references = refrence.get_mulitiple_references(reference_list, db=db)
    existing_references_names = set(ref.url for ref in existing_references)
    not_existing_references = set(reference_list) - existing_references_names
    if not_existing_references:
        new_references = refrence.create_mulitiple_references(
            not_existing_references, db=db
        )
        existing_references.append(new_references)

    return existing_references


def create_question_service(question: CreateQuestion, db: Session) -> Question:
    reference_objects = handle_question_reference(question.references, db=db)
    tag_objects = handle_tags(question.tags, db=db)
    question_object = questions.create_question(
        question_text=question.question_text,
        answer=question.answer,
        level=question.level,
        tags=tag_objects,
        references=reference_objects,
        db=db,
    )
    return question_object


def update_question_service(question: UpdateQuestion, db: Session) -> Question:
    reference_objects = handle_question_reference(question.references, db=db)
    tag_objects = handle_tags(question.tags, db=db)
    question_object = questions.update_question(
        question_id=question.id,
        question_text=question.question_text,
        answer=question.answer,
        level=question.level,
        tags=tag_objects,
        references=reference_objects,
        db=db,
    )
    return question_object
