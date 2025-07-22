from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from app.core.domain import User
from app.core.security import IPasswordHasher, ITokenProvider
from app.db.models import User as UserModel
from app.dependencies import get_session
from app.infrastructure.security import JWTTokenProvider, PasslibHasher
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
async def override_session_dependency(session):
    app.dependency_overrides[get_session] = lambda: session


@pytest.fixture(autouse=True)
async def cleanup_overrides():
    yield
    app.dependency_overrides = {}


@pytest.fixture(name="client")
async def get_async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


class TestLogoutEndpoint:
    @pytest.fixture(autouse=True, scope="class")
    @classmethod
    def init_class(cls):
        cls.token_provider: ITokenProvider = JWTTokenProvider()
        cls.password_hasher: IPasswordHasher = PasslibHasher()

    @pytest.fixture(autouse=True)
    def init_method(self, session: AsyncSession):
        self.session = session
        self.user_counter: int = 0

    async def create_user(self, **kwargs) -> User:
        self.user_counter += 1
        password = f"Test{self.user_counter}Pass"
        user = UserModel(
            email=f"test{self.user_counter}@gmail.com",
            password=self.password_hasher.hash(password),
            **kwargs,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return User(**{f: getattr(user, f) for f in User.__dataclass_fields__})

    async def test_without_tokens(self, client: AsyncClient):
        response = await client.post("/auth/logout")
        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Not authenticated"}

    async def test_with_valid_tokens(self, client: AsyncClient):
        user = await self.create_user()
        access_token = self.token_provider.create_access_token(user)
        refresh_token = self.token_provider.create_refresh_token(user)

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
        refresh_token = self.token_provider.create_refresh_token(user)

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
        access_token = self.token_provider.create_refresh_token(user)

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
        access_token = self.token_provider.create_access_token(user)
        refresh_token = self.token_provider.create_refresh_token(user)

        response = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {access_token.token}"},
            cookies={"refresh": refresh_token.token},
        )

        assert response.status_code == 404
        assert response.json() == {
            "detail": f"User with {user.email} email does not exist"
        }

    @pytest.mark.parametrize(
        "token_live_duration",
        [REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES],
    )
    async def test_access_token_expired(
        self, token_live_duration: int, client: AsyncClient
    ):
        user = await self.create_user()
        access_token = self.token_provider.create_access_token(user)
        refresh_token = self.token_provider.create_refresh_token(user)

        with freeze_time(datetime.now() + timedelta(minutes=token_live_duration + 5)):
            response = await client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {access_token.token}"},
                cookies={"refresh": refresh_token.token},
            )

        assert response.status_code == 401
        assert response.json() == {"detail": "Token is expired"}
