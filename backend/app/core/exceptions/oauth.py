from .generic import BaseExceptionError


class OAuthError(BaseExceptionError):
    """Base exception for OAuth errors"""

    pass


class OAuthProviderError(OAuthError):
    """Exception raised when OAuth provider returns an error"""

    pass


class OAuthTokenExchangeError(OAuthError):
    """Exception raised when token exchange fails"""

    pass


class OAuthStateMismatchError(OAuthError):
    """Exception raised when OAuth state doesn't match"""

    pass


class OAuthAccountAlreadyLinkedError(OAuthError):
    """Exception raised when OAuth account is already linked to another user"""

    pass
