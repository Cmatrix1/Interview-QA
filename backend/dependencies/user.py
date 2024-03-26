from jose import JWTError
from sqlalchemy.orm import Session
from fastapi import Request, Depends, status

from core.config import settings
from utils.security import token as token_utils
from utils.security.oauth2 import OAuth2PasswordBearerWithCookie
from utils.exceptions.auth import CredentialsException

from db.session import get_db
from db.repository.user import get_user_for_authentication


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")


def get_current_user(token: str, db: Session):
    credentials_exception = CredentialsException()
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

    user = get_user_for_authentication(username=username, db=db)
    return user



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
