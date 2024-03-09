from utils.exceptions.base import AppBaseException


class UserAlreadyExistsException(AppBaseException):
    message = "This Username Already Exists."
    
    
class UserNotFoundException(AppBaseException):
    message = "User with this username not found."