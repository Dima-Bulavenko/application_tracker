from .generic import BaseExceptionError


class TokenError(BaseExceptionError):
    pass


class TokenInvalidError(TokenError):
    pass


class TokenExpireError(TokenError):
    pass
