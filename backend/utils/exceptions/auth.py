from fastapi import status
from utils.exceptions.base import AppBaseException


class CredentialsException(AppBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}


class NotAuthenticatedException(AppBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Not authenticated"
    headers = {"WWW-Authenticate": "Bearer"}
