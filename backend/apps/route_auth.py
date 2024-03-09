import json
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import APIRouter, Request, Form, Depends, status
from pydantic import ValidationError as PydaticValidationError

from core.config import settings
from schemas.user import UserCreate
from utils import exceptions
from utils.security import hashing, token as token_utils

from db.session import get_db
from db.repository.user import create_new_user, get_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        user = UserCreate(username=username, password=password)
    except PydaticValidationError as e:
        errors = {data['loc'][0]: data['msg'] for data in json.loads(e.json())}
        return templates.TemplateResponse("auth/register.html", {"request": request, "errors": errors})

    try:
        create_new_user(user=user, db=db)
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    except exceptions.UserAlreadyExistsException as exp:
        errors = {'username': exp.message}
        return templates.TemplateResponse("auth/register.html", {"request": request, "errors": errors})


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user(username=username, db=db, raise_exceptions=False)
    if user and hashing.verify_password(password, user.password):
        access_token = token_utils.create_access_token(data={"sub": username})
        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key=settings.COOKIE_NAME,
                            value=f"Bearer {access_token}", httponly=True)
        return response

    errors = {'error': "Username or Password is Not Correct"}
    return templates.TemplateResponse("auth/login.html", {"request": request, "errors": errors},
                                      status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/auth/logout", response_class=HTMLResponse)
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.COOKIE_NAME)
    return response
