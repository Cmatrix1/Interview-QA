from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    questions = [
        {
            'question': 'What is Python?',
            'answer': 'Python is a high-level programming language...',
            'created_at': '2024-02-25',
            'tags': ['Python', 'Programming', 'Language']
        },
        {
            'question': 'What is AI?',
            'answer': 'AI stands for Artificial Intelligence...',
            'created_at': '2024-02-24',
            'tags': ['AI', 'Technology']
        },
        {
            'question': 'How to sort a list in Python?',
            'answer': 'You can sort a list in Python using the sort() method...',
            'created_at': '2024-02-23',
            'tags': ['Python', 'Programming']
        }
    ]

    return templates.TemplateResponse("questions/list.html", {"request": request, "questions": questions})
