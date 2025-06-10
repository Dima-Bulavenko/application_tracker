from .generic import BaseExceptionError


class TokenInvalidError(BaseExceptionError):
    pass


class TokenExpireError(TokenInvalidError):
    pass
