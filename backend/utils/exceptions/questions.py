from utils.exceptions.base import AppBaseException
from fastapi import status


class QuestionNotFoundException(Exception):
    ...