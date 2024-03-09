from apps import route_questions, route_auth
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@app_router.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


app_router.include_router(
    route_questions.router, prefix="/question", tags=["questions"], include_in_schema=False
)

app_router.include_router(
    route_auth.router, prefix="/auth", tags=["auth"], include_in_schema=False
)
