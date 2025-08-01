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


class TestApplicationDelete(BaseTest):
    async def test_delete_application_success(self, client: AsyncClient):
        """Test successful application deletion."""
        user = await self.create_user()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)
        assert application.id is not None

        response = await client.delete(
            f"/applications/{application.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 204
        assert response.content == b""

        # Verify application was actually deleted
        database_entity = await self.get_application(application.id)
        assert database_entity is None

    async def test_delete_with_non_existent_application(self, client: AsyncClient):
        """Test delete with non-existent application ID."""
        user = await self.create_user()
        access_token = self.token_provider.create_access_token(user)

        response = await client.delete(
            "/applications/999999",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Application with 999999 id is not found"}

    @pytest.mark.parametrize(
        "header, error_message",
        [({"Authorization": "Bearer invalid_token"}, "Token invalid"), (None, "Not authenticated")],
    )
    async def test_delete_with_not_authenticated_user(
        self, header: dict | None, error_message: str, client: AsyncClient
    ):
        """Test delete without proper authentication."""
        application = await self.create_application()

        response = await client.delete(f"/applications/{application.id}", headers=header)

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": f"{error_message}"}

    async def test_delete_with_non_active_user(self, client: AsyncClient):
        """Test delete with inactive user account."""
        user = await self.create_user(is_active=False)
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)

        response = await client.delete(
            f"/applications/{application.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 403
        assert response.json() == {"detail": "User account is not activated"}

    async def test_delete_with_non_authorized_user(self, client: AsyncClient):
        """Test delete by user who doesn't own the application."""
        user = await self.create_user()
        another_user = await self.create_user()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(another_user)

        response = await client.delete(
            f"/applications/{application.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 403
        assert response.json() == {
            "detail": f"User with {another_user.id} id is not authorized to delete this application"
        }

    async def test_delete_multiple_applications(self, client: AsyncClient):
        """Test deleting multiple applications owned by the same user."""
        user = await self.create_user()
        application1 = await self.create_application(user.id)
        application2 = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)
        assert application1.id is not None
        assert application2.id is not None

        # Delete first application
        response1 = await client.delete(
            f"/applications/{application1.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )
        assert response1.status_code == 204

        # Delete second application
        response2 = await client.delete(
            f"/applications/{application2.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )
        assert response2.status_code == 204

        # Verify both applications were deleted
        database_entity1 = await self.get_application(application1.id)
        database_entity2 = await self.get_application(application2.id)
        assert database_entity1 is None
        assert database_entity2 is None

    async def test_delete_application_twice(self, client: AsyncClient):
        """Test attempting to delete the same application twice."""
        user = await self.create_user()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)

        # First deletion should succeed
        response1 = await client.delete(
            f"/applications/{application.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )
        assert response1.status_code == 204

        # Second deletion should fail with 404
        response2 = await client.delete(
            f"/applications/{application.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )
        assert response2.status_code == 404
        assert response2.json() == {"detail": f"Application with {application.id} id is not found"}


class TestApplicationGetById(BaseTest):
    async def test_get_application_success(self, client: AsyncClient):
        """Test successful retrieval of application by ID."""
        user = await self.create_user()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)
        assert application.id is not None

        response = await client.get(
            f"/applications/{application.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == application.id
        assert response_data["role"] == application.role
        assert response_data["user_id"] == user.id
        assert response_data["company_id"] == application.company_id

    async def test_get_with_non_existent_application(self, client: AsyncClient):
        """Test get with non-existent application ID."""
        user = await self.create_user()
        access_token = self.token_provider.create_access_token(user)

        response = await client.get(
            "/applications/999999",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Application with 999999 id is not found"}

    @pytest.mark.parametrize(
        "header, error_message",
        [({"Authorization": "Bearer invalid_token"}, "Token invalid"), (None, "Not authenticated")],
    )
    async def test_get_with_not_authenticated_user(self, header: dict | None, error_message: str, client: AsyncClient):
        """Test get without proper authentication."""
        application = await self.create_application()

        response = await client.get(f"/applications/{application.id}", headers=header)

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": f"{error_message}"}

    async def test_get_with_non_active_user(self, client: AsyncClient):
        """Test get with inactive user account."""
        user = await self.create_user(is_active=False)
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(user)

        response = await client.get(
            f"/applications/{application.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 403
        assert response.json() == {"detail": "User account is not activated"}

    async def test_get_with_non_authorized_user(self, client: AsyncClient):
        """Test get by user who doesn't own the application."""
        user = await self.create_user()
        another_user = await self.create_user()
        application = await self.create_application(user.id)
        access_token = self.token_provider.create_access_token(another_user)

        response = await client.get(
            f"/applications/{application.id}",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 403
        assert response.json() == {
            "detail": f"User with {another_user.id} id is not authorized to access this application"
        }
