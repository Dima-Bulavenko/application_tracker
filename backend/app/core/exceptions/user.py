from .generic import AlreadyExistError, BaseExceptionError, NotFoundError


class UserNotFoundError(NotFoundError):
    pass


class UserAlreadyExistError(AlreadyExistError):
    pass


class UserNotAuthorizedError(BaseExceptionError):
    pass


class UserAlreadyActivatedError(BaseExceptionError):
    pass
