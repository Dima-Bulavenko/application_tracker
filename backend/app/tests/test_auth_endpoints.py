from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from httpx import AsyncClient

from app import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from app.core.domain import User

from .base import BaseTest


class TestLoginEndpoint(BaseTest):
    async def test_with_valid_credentials(self, client: AsyncClient):
        user = await self.create_user()

        response = await client.post(
            "/auth/login",
            data={"username": user.email, "password": self.get_user_password()},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["access_token"] is not None

        # Check that refresh token is set in cookies
        assert "refresh" in response.cookies
        refresh_cookie = response.cookies["refresh"]
        assert refresh_cookie is not None
        assert refresh_cookie != ""

    async def test_with_not_existent_user(self, client: AsyncClient):
        response = await client.post(
            "/auth/login",
            data={"username": "nonexistent@example.com", "password": "ValidPass123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Not authenticated"}

    @pytest.mark.parametrize("invalid_email", ["invalidemail", "user@.com", "user@domain", "@domain.com"])
    async def test_with_invalid_email(self, invalid_email: str, client: AsyncClient):
        response = await client.post(
            "/auth/login",
            data={"username": invalid_email, "password": "ValidPass123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        detail = response.json().get("detail", [])
        assert response.status_code == 422
        assert len(detail) == 1
        assert detail[0]["loc"] == ["body", "username"]
        assert detail[0]["type"] == "value_error"

    @pytest.mark.parametrize("invalid_password", ["short", "alllowercase", "12345678", "NoDigitsHere"])
    async def test_with_invalid_password(self, invalid_password: str, client: AsyncClient):
        user = await self.create_user()

        response = await client.post(
            "/auth/login",
            data={"username": user.email, "password": invalid_password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        detail = response.json().get("detail", [])
        assert response.status_code == 422
        assert len(detail) == 1
        assert detail[0]["loc"] == ["body", "password"]
        assert detail[0]["type"] == "string_pattern_mismatch"

    async def test_with_wrong_password(self, client: AsyncClient):
        user = await self.create_user()

        response = await client.post(
            "/auth/login",
            data={"username": user.email, "password": "WrongPass123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Not authenticated"}

    async def test_with_missing_credentials(self, client: AsyncClient):
        response = await client.post("/auth/login")
        assert response.status_code == 422


class TestLogoutEndpoint(BaseTest):
    async def test_without_tokens(self, client: AsyncClient):
        response = await client.post("/auth/logout")
        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Not authenticated"}

    async def test_with_valid_tokens(self, client: AsyncClient):
        user = await self.create_user()
        access_token = self.create_access_token(user)
        refresh_token = self.create_refresh_token(user)

        response = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {access_token.token}"},
            cookies={"refresh": refresh_token.token},
        )
        assert response.status_code == 204
        assert "Max-Age=0" in response.headers.get("set-cookie", "")
        assert "refresh" in response.headers.get("set-cookie", "")

    async def test_with_invalid_access_token(self, client: AsyncClient):
        user = await self.create_user()
        refresh_token = self.create_refresh_token(user)

        response = await client.post(
            "/auth/logout",
            headers={"Authorization": "Bearer invalid_token"},
            cookies={"refresh": refresh_token.token},
        )
        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Token is not valid"}

    async def test_with_invalid_refresh_token(self, client: AsyncClient):
        user = await self.create_user()
        access_token = self.create_refresh_token(user)

        response = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {access_token.token}"},
            cookies={"refresh": "invalid_refresh_token"},
        )
        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Token is not valid"}

    async def test_user_does_not_exits(self, client: AsyncClient):
        user = User(id=1, email="notexistinguser@gmail.com", password="password")
        access_token = self.create_access_token(user)
        refresh_token = self.create_refresh_token(user)

        response = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {access_token.token}"},
            cookies={"refresh": refresh_token.token},
        )

        assert response.status_code == 404
        assert response.json() == {"detail": f"User with {user.email} email does not exist"}

    @pytest.mark.parametrize(
        "token_live_duration",
        [REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES],
    )
    async def test_access_token_expired(self, token_live_duration: int, client: AsyncClient):
        user = await self.create_user()
        access_token = self.create_access_token(user)
        refresh_token = self.create_refresh_token(user)

        with freeze_time(datetime.now() + timedelta(minutes=token_live_duration + 5)):
            response = await client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {access_token.token}"},
                cookies={"refresh": refresh_token.token},
            )

        assert response.status_code == 401
        assert response.json() == {"detail": "Token is expired"}
