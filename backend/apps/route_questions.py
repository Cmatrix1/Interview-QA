from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.exceptions import HTTPException 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.questions import list_questions, detail_questions
from dependencies.user import get_current_user_from_token, get_current_user_from_cookie
from db.models.user import User
from schemas.question import CreateQuestion, UpdateQuestion
from dependencies.questions import validate_question_id
from services.question import create_question_service, update_question_service
from utils.exceptions.questions import QuestionNotFoundException


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def question_list(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user_from_cookie)):
    questions = list_questions(db=db)
    return templates.TemplateResponse(
        "questions/list.html", {"request": request, "questions": questions, "user":user}
    )


@router.get("/detail/{id}", response_class=HTMLResponse)
def question_detail(request: Request, id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_from_cookie)):
    question = detail_questions(id=id, db=db)
    return templates.TemplateResponse(
        "questions/detail.html", {"request": request, "question": question}
    )


@router.get("/create", response_class=HTMLResponse)
def question_create(
    request: Request, user: User = Depends(get_current_user_from_token)
):
    return templates.TemplateResponse("questions/create.html", {"request": request})


@router.post("/create", response_class=HTMLResponse)
def question_create(
    request: Request,
    db: Session = Depends(get_db),
    question_text: str = Form(...),
    answer: str = Form(...),
    level: str = Form(...),
    tags: list[str] = Form(...),
    references: list[str] = Form(...),
    user: User = Depends(get_current_user_from_token),
):
    question = CreateQuestion(question_text=question_text, answer=answer, level=level, tags=tags, references=references)
    question_object = create_question_service(question=question, db=db)
    return RedirectResponse(
        url=request.url_for('question_detail', id=question_object.id), 
        status_code=status.HTTP_303_SEE_OTHER
        )


@router.get("/update/{question_id}", response_class=HTMLResponse)
def question_update(
    request: Request,
    question_id: int = Depends(validate_question_id),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
):
    question = detail_questions(id=question_id, db=db)
    return templates.TemplateResponse(
        "questions/update.html", {"request": request, "question": question}
    )


@router.post("/update/{question_id}", response_class=HTMLResponse)
def question_update(
    request: Request,
    question_id: int,
    db: Session = Depends(get_db),
    question_text: str = Form(...),
    answer: str = Form(...),
    level: str = Form(...),
    tags: list[str] = Form(...),
    references: list[str] = Form(...),
    user: User = Depends(get_current_user_from_token), # TODO: check user is admin with depends
):
    question = UpdateQuestion(id=question_id, question_text=question_text, answer=answer, level=level, tags=tags, references=references)

    try:
        question_object = update_question_service(question=question, db=db)
    except QuestionNotFoundException as exp:
        raise HTTPException(status_code=404, detail=str(exp))
    
    return RedirectResponse(
        url=request.url_for('question_detail', id=question_object.id), 
        status_code=status.HTTP_303_SEE_OTHER
        )
