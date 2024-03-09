import json
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import APIRouter, Request, Form, Depends, status
from pydantic import ValidationError as PydaticValidationError

from core.config import settings
from schemas.user import UserCreate
from utils import exceptions
from utils.security import hashing, token as token_utils
from utils.security.oauth2 import OAuth2PasswordBearerWithCookie
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


def get_current_user(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        return None
    token = token.removeprefix("Bearer").strip()
    try:
        username = token_utils.get_username_from_token(token)        
    except JWTError as e:
        credentials_exception.detail = str(e)
        raise credentials_exception
    if username is None:
        raise credentials_exception

    user = get_user(username=username, db=db)
    return user


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")

def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user from the cookies in a request.

    Use this function when you want to lock down a route so that only 
    authenticated users can see access the route.
    """
    user = get_current_user(token, db)
    return user


def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    """
    Get the current user from the cookies in a request.

    Use this function from inside other routes to get the current user. Good
    for views that should work for both logged in, and not logged in users.
    """
    token = request.cookies.get(settings.COOKIE_NAME)
    user = get_current_user(token, db)
    return user
