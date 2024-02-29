from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.questions import list_questions, detail_questions


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def question_list(request: Request, db: Session = Depends(get_db)):
    questions = list_questions(db=db)
    return templates.TemplateResponse("questions/list.html",
                                      {"request": request, "questions": questions})


@router.get("/detail/{id}", response_class=HTMLResponse)
def question_detail(request: Request, id: int, db: Session = Depends(get_db)):
    question = detail_questions(id=id, db=db)
    return templates.TemplateResponse("questions/detail.html", {"request": request, "question": question})


@router.get("/create", response_class=HTMLResponse)
def question_create(request: Request):
    return templates.TemplateResponse("questions/create.html", {"request": request})


@router.post("/create", response_class=HTMLResponse)
def question_create(request: Request, db: Session = Depends(get_db), question_text: str = Form(...), answer: str = Form(...), level: str = Form(...), tags: list[str] = Form(...), references: list[str] = Form(...)):
    print(f"{question_text=}, {answer=}, {level=}, {tags=}, {references=}")
    # Implement the logic of create question
    return templates.TemplateResponse("questions/create.html", {"request": request})


@router.get("/update/{id}", response_class=HTMLResponse)
def question_update(request: Request, id: int, db: Session = Depends(get_db)):
    question = detail_questions(id=id, db=db)
    return templates.TemplateResponse("questions/update.html", {"request": request, "question": question})

@router.get("/update/{id}", response_class=HTMLResponse)
def question_update(request: Request, db: Session = Depends(get_db), question_text: str = Form(...), answer: str = Form(...), level: str = Form(...), tags: list[str] = Form(...), references: list[str] = Form(...)):
    question = detail_questions(id=id, db=db)
    print(f"{question_text=}, {answer=}, {level=}, {tags=}, {references=}")
    # Implement the logic of update question
    return templates.TemplateResponse("questions/update.html", {"request": request, "question": question})
