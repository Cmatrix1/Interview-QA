

class AppBaseException(Exception):
    def __init__(self, message: str = None):
        if getattr(self, 'message', None) is None :
            if message is not None:
                self.message = message
            else:
                raise ValueError('The AppBaseException must have a message attribute.')
