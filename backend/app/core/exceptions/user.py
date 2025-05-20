from .generic import AlreadyExistError, NotFoundError


class UserNotFoundError(NotFoundError):
    pass


class UserAlreadyExistError(AlreadyExistError):
    pass
