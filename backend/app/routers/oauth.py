from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse

from app import FRONTEND_ORIGIN, Tags
from app.core.domain.user import OAuthProvider
from app.core.dto.oauth import OAuthAuthorizeResponse
from app.core.exceptions import UserAlreadyExistError
from app.core.exceptions.oauth import (
    OAuthAccountAlreadyLinkedError,
    OAuthError,
    OAuthProviderError,
    OAuthTokenExchangeError,
)
from app.core.services import OAuthService
from app.dependencies import RefreshTokenServiceDep, SessionDep
from app.infrastructure.oauth import GoogleOAuthProvider
from app.infrastructure.repositories import UserSQLAlchemyRepository
from app.infrastructure.security import AccessTokenStrategy

from .auth import RefreshTokenSettings

router = APIRouter(prefix="/auth/oauth", tags=[Tags.AUTHENTICATION])


def get_oauth_service(session: SessionDep, refresh_token_service: RefreshTokenServiceDep) -> OAuthService:
    """Dependency for OAuth service"""
    return OAuthService(
        user_repo=UserSQLAlchemyRepository(session),
        access_strategy=AccessTokenStrategy(),
        refresh_token_service=refresh_token_service,
    )


OAuthServiceDep = Annotated[OAuthService, Depends(get_oauth_service)]


@router.get("/google/authorize")
async def google_authorize(oauth_service: OAuthServiceDep, response: Response) -> OAuthAuthorizeResponse:
    """Initiate Google OAuth flow

    Redirects user to Google authorization page.
    State token is stored in HTTPOnly cookie for CSRF protection.
    """
    provider = GoogleOAuthProvider()
    state = oauth_service.generate_state_token()

    authorization_url = provider.get_authorization_url(state)

    response.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=600,
    )

    return OAuthAuthorizeResponse(authorization_url=authorization_url, state=state)


@router.get("/google/callback")
async def google_callback(
    code: str,
    state: str,
    response: Response,
    oauth_service: OAuthServiceDep,
    oauth_state_cookie: str | None = Cookie(None, alias="oauth_state"),
) -> RedirectResponse:
    """Handle Google OAuth callback

    This endpoint receives the authorization code from Google and:
    1. Validates the state token (CSRF protection via cookie comparison)
    2. Exchanges code for access token
    3. Fetches user info from Google
    4. Creates or logs in user
    5. Issues JWT tokens
    6. Redirects to frontend with access token

    The refresh token is set as an HTTPOnly secure cookie.
    """
    if not oauth_state_cookie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing state cookie",
        )

    if state != oauth_state_cookie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="State mismatch - possible CSRF attack",
        )

    response.delete_cookie(key="oauth_state")

    try:
        provider = GoogleOAuthProvider()
        tokens, is_new_user = await oauth_service.authenticate_oauth_user(
            oauth_provider=provider, provider_type=OAuthProvider.GOOGLE, code=code, state=state
        )

        access_token, refresh_token = tokens

        response.set_cookie(
            **asdict(RefreshTokenSettings()), value=refresh_token.token, expires=refresh_token.payload.exp
        )

        redirect_url = (
            f"{FRONTEND_ORIGIN}/auth/callback?"
            f"access_token={access_token.token}&"
            f"user_id={access_token.payload.user_id}&"
            f"email={access_token.payload.user_email}&"
            f"is_new_user={str(is_new_user).lower()}"
        )

        return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    except OAuthTokenExchangeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except OAuthProviderError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e)) from e
    except OAuthAccountAlreadyLinkedError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UserAlreadyExistError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except OAuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
