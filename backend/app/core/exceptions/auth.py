from .generic import BaseExceptionError


class TokenError(BaseExceptionError):
    pass


class TokenInvalidError(TokenError):
    pass


class TokenExpireError(TokenError):
    pass


class RefreshTokenRevokedError(TokenError):
    """Raised when attempting to use a revoked refresh token."""

    pass


class RefreshTokenReuseError(TokenError):
    """Raised when attempting to reuse a refresh token that has already been used.

    This indicates a potential security breach and triggers revocation of the entire token family.
    """

    pass
