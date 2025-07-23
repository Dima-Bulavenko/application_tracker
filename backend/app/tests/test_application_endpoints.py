from datetime import datetime

import pytest
from httpx import AsyncClient

from .base import BaseTest


class TestApplicationUpdate(BaseTest):
    @pytest.mark.parametrize(
        "field,value",
        [
            ("role", "Updated Role"),
            ("status", "interview"),
            ("status", "offer"),
            ("status", "rejected"),
            ("work_type", "part_time"),
            ("work_type", "internship"),
            ("work_type", "contract"),
            ("work_type", "other"),
            ("work_location", "remote"),
            ("work_location", "hybrid"),
            ("work_location", "on_site"),
            ("note", "gav"),
            ("application_url", "https://example.com/updated-application"),
        ],
    )
    async def test_update_application(self, field: str, value: str, client: AsyncClient):
        user = await self.create_user()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)
        assert application.id is not None

        response = await client.patch(
            f"/applications/{application.id}",
            json={field: value},
            headers={"Authorization": f"Bearer {access_token.token}"},
        )
        database_entity = await self.get_application(application.id)
        response_data = response.json()
        assert database_entity is not None
        assert response.status_code == 200
        assert response_data[field] == value
        assert datetime.fromisoformat(response_data["time_create"]) == application.time_create
        assert datetime.fromisoformat(response_data["time_update"]) is not application.time_update

    async def test_update_with_empty_body(self, client: AsyncClient):
        user = await self.create_user()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)
        assert application.id is not None

        response = await client.patch(
            f"/applications/{application.id}",
            json={},
            headers={"Authorization": f"Bearer {access_token.token}"},
        )
        response_data = response.json()
        assert response.status_code == 200

        assert response_data["role"] == application.role
        assert response_data["company_id"] == application.company_id
        assert response_data["user_id"] == application.user_id
        assert response_data["id"] == application.id
        assert response_data["status"] == application.status.value
        assert response_data["work_type"] == application.work_type.value
        assert response_data["work_location"] == application.work_location.value
        assert response_data["note"] == application.note
        assert response_data["application_url"] == application.application_url
        assert datetime.fromisoformat(response_data["time_create"]) == application.time_create
        assert datetime.fromisoformat(response_data["time_update"]) == application.time_update

    @pytest.mark.parametrize(
        "header, error_message",
        [({"Authorization": "Bearer invalid_token"}, "Token invalid"), (None, "Not authenticated")],
    )
    async def test_with_not_authenticated_user(self, header: dict | None, error_message: str, client: AsyncClient):
        application = await self.create_application()
        response = await client.patch(f"/applications/{application.id}", json={"role": "Updated Role"}, headers=header)
        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": f"{error_message}"}

    async def test_with_non_existent_application(self, client: AsyncClient):
        user = await self.create_user()
        access_token = self.token_provider.create_access_token(user)
        response = await client.patch(
            "/applications/999999",
            json={"role": "Updated Role"},
            headers={"Authorization": f"Bearer {access_token.token}"},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Application with 999999 id is not found"}

    async def test_with_non_active_user(self, client: AsyncClient):
        user = await self.create_user(is_active=False)
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)

        response = await client.patch(
            f"/applications/{application.id}",
            json={"role": "Updated Role"},
            headers={"Authorization": f"Bearer {access_token.token}"},
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "User account is not activated"}

    async def test_with_non_authorized_user(self, client: AsyncClient):
        user = await self.create_user()
        another_user = await self.create_user()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(another_user)

        response = await client.patch(
            f"/applications/{application.id}",
            json={"role": "Updated Role"},
            headers={"Authorization": f"Bearer {access_token.token}"},
        )
        assert response.status_code == 403
        assert response.json() == {
            "detail": f"User with {another_user.id} id is not authorized to update this application"
        }

    async def test_with_existent_company(self, client: AsyncClient):
        user = await self.create_user()
        company = await self.create_company()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)

        response = await client.patch(
            f"/applications/{application.id}",
            json={"company": {"name": company.name}},
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["company_id"] == company.id

    async def test_with_non_existent_company(self, client: AsyncClient):
        user = await self.create_user()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)
        company_name = "NonExistentCompany"

        response = await client.patch(
            f"/applications/{application.id}",
            json={"company": {"name": company_name}},
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 200
        company_id = response.json()["company_id"]
        company = await self.get_company(company_id)
        assert company is not None
        assert company.name == company_name

    async def test_with_same_company(self, client: AsyncClient):
        user = await self.create_user()
        company = await self.create_company()
        application = await self.create_application(user.id, company_id=company.id)
        access_token = self.token_provider.create_access_token(user)

        response = await client.patch(
            f"/applications/{application.id}",
            json={"company": {"name": company.name}},
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["company_id"] == company.id
