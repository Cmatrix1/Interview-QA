from fastapi.exceptions import HTTPException


class AppBaseException(HTTPException):
    def __init__(self, *args, **kwargs):
        if not getattr(self, 'detail', None):
            super(AppBaseException, self).__init__(*args, **kwargs)
