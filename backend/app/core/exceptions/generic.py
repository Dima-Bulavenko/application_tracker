class BaseExceptionError(Exception):
    pass


class NotFoundError(BaseExceptionError):
    pass


class AlreadyExistError(BaseExceptionError):
    pass


class InvalidPasswordError(BaseException):
    pass
