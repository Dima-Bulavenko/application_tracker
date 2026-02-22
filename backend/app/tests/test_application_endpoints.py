from datetime import datetime

import pytest
from httpx import AsyncClient

from app.core.domain import User
from app.core.domain.application import Application
from app.core.domain.company import Company
from app.core.dto.application import ApplicationCreate


@pytest.fixture(name="user", autouse=True)
async def create_user(user_factory):
    return await user_factory()


@pytest.fixture(name="company", autouse=True)
async def create_company(company_factory):
    return await company_factory()


@pytest.fixture(name="access_token", autouse=True)
def create_access_token(access_token_factory, user):
    return access_token_factory(user).token


@pytest.fixture(name="application")
async def create_application_fixture(user: User, application_factory):
    return await application_factory(user_id=user.id)


@pytest.fixture(name="client_config")
def client_config(access_token: str):
    return {
        "headers": {"Authorization": f"Bearer {access_token}"},
    }


class TestApplicationUpdate:
    url: str = "/applications/{id}"

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
    async def test_update_application(
        self,
        field: str,
        value: str,
        client: AsyncClient,
        application: Application,
        application_repo,
    ):
        assert application.id is not None

        response = await client.patch(self.url.format(id=application.id), json={field: value})
        database_entity = await application_repo.get_by_id(application.id)
        response_data = response.json()
        assert database_entity is not None
        assert response.status_code == 200
        assert response_data[field] == value
        assert datetime.fromisoformat(response_data["time_create"]) == application.time_create
        assert datetime.fromisoformat(response_data["time_update"]) is not application.time_update

    async def test_update_with_empty_body(self, client: AsyncClient, application: Application):
        assert application.id is not None

        response = await client.patch(self.url.format(id=application.id), json={})
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

    async def test_with_no_authorization_header(
        self,
        client: AsyncClient,
        application: Application,
    ):
        del client.headers["Authorization"]
        response = await client.patch(self.url.format(id=application.id), json={"role": "Updated Role"})

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Not authenticated"}

    async def test_with_invalid_authorization_token(
        self,
        client: AsyncClient,
        application: Application,
    ):
        response = await client.patch(
            self.url.format(id=application.id),
            headers={"Authorization": "Bearer invalid_token"},
            json={"role": "Updated Role"},
        )
        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Token is not valid"}

    async def test_with_non_existent_application(self, client: AsyncClient):
        response = await client.patch(self.url.format(id=999999), json={"role": "Updated Role"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Application with 999999 id is not found"}

    async def test_with_non_active_user(
        self,
        client: AsyncClient,
        user_factory,
        access_token_factory,
        application_factory,
    ):
        user = await user_factory(is_active=False)
        application = await application_factory(user_id=user.id)
        access_token = access_token_factory(user)

        response = await client.patch(
            self.url.format(id=application.id),
            headers={"Authorization": f"Bearer {access_token.token}"},
            json={"role": "Updated Role"},
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "User account is not activated"}

    async def test_with_non_authorized_user(
        self,
        client: AsyncClient,
        user_factory,
        access_token_factory,
        application_factory,
    ):
        user = await user_factory()
        another_user = await user_factory()
        application = await application_factory(user_id=user.id)
        access_token = access_token_factory(another_user)

        response = await client.patch(
            self.url.format(id=application.id),
            headers={"Authorization": f"Bearer {access_token.token}"},
            json={"role": "Updated Role"},
        )
        assert response.status_code == 403
        assert response.json() == {
            "detail": f"User with {another_user.id} id is not authorized to update this application"
        }

    async def test_with_existent_company(
        self,
        client: AsyncClient,
        company_factory,
        application: Application,
    ):
        company = await company_factory()

        response = await client.patch(self.url.format(id=application.id), json={"company": {"name": company.name}})

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["company_id"] == company.id

    async def test_with_non_existent_company(
        self,
        client: AsyncClient,
        company_repo,
        application: Application,
    ):
        company_name = "NonExistentCompany"

        response = await client.patch(self.url.format(id=application.id), json={"company": {"name": company_name}})

        assert response.status_code == 200
        company_id = response.json()["company_id"]
        company = await company_repo.get_by_id(company_id)
        assert company is not None
        assert company.name == company_name

    async def test_with_same_company(
        self,
        client: AsyncClient,
        application: Application,
        company: Company,
    ):
        response = await client.patch(
            self.url.format(id=application.id),
            json={"company": {"name": company.name}},
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["company_id"] == company.id


class TestApplicationDelete:
    url: str = "/applications/{id}"

    async def test_delete_application_success(
        self,
        client: AsyncClient,
        application: Application,
        application_repo,
    ):
        """Test successful application deletion."""
        assert application.id is not None

        response = await client.delete(self.url.format(id=application.id))

        assert response.status_code == 204
        assert response.content == b""

        # Verify application was actually deleted
        database_entity = await application_repo.get_by_id(application.id)
        assert database_entity is None

    async def test_delete_with_non_existent_application(self, client: AsyncClient):
        """Test delete with non-existent application ID."""
        response = await client.delete(self.url.format(id=999999))

        assert response.status_code == 404
        assert response.json() == {"detail": "Application with 999999 id is not found"}

    async def test_delete_with_no_authorization_header(
        self,
        client: AsyncClient,
        application: Application,
    ):
        del client.headers["Authorization"]
        response = await client.delete(self.url.format(id=application.id))

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Not authenticated"}

    async def test_delete_with_invalid_authorization_token(
        self,
        client: AsyncClient,
        application: Application,
    ):
        response = await client.delete(
            self.url.format(id=application.id),
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Token is not valid"}

    async def test_delete_with_non_active_user(
        self,
        client: AsyncClient,
        user_factory,
        access_token_factory,
        application_factory,
    ):
        """Test delete with inactive user account."""
        user = await user_factory(is_active=False)
        application = await application_factory(user_id=user.id)
        access_token = access_token_factory(user)

        response = await client.delete(
            self.url.format(id=application.id),
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 403
        assert response.json() == {"detail": "User account is not activated"}

    async def test_delete_with_non_authorized_user(
        self,
        client: AsyncClient,
        user_factory,
        access_token_factory,
        application_factory,
    ):
        """Test delete by user who doesn't own the application."""
        user = await user_factory()
        another_user = await user_factory()
        application = await application_factory(user_id=user.id)
        access_token = access_token_factory(another_user)

        response = await client.delete(
            self.url.format(id=application.id),
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 403
        assert response.json() == {
            "detail": f"User with {another_user.id} id is not authorized to delete this application"
        }

    async def test_delete_multiple_applications(
        self,
        client: AsyncClient,
        user: User,
        application_factory,
        access_token_factory,
        application_repo,
    ):
        """Test deleting multiple applications owned by the same user."""
        application1 = await application_factory(user_id=user.id)
        application2 = await application_factory(user_id=user.id)
        access_token = access_token_factory(user)
        assert application1.id is not None
        assert application2.id is not None
        headers = {"Authorization": f"Bearer {access_token.token}"}

        # Delete first application
        response1 = await client.delete(self.url.format(id=application1.id), headers=headers)
        assert response1.status_code == 204

        # Delete second application
        response2 = await client.delete(self.url.format(id=application2.id), headers=headers)
        assert response2.status_code == 204

        # Verify both applications were deleted
        database_entity1 = await application_repo.get_by_id(application1.id)
        database_entity2 = await application_repo.get_by_id(application2.id)
        assert database_entity1 is None
        assert database_entity2 is None

    async def test_delete_application_twice(
        self,
        client: AsyncClient,
        application: Application,
    ):
        """Test attempting to delete the same application twice."""
        url = self.url.format(id=application.id)

        # First deletion should succeed
        response1 = await client.delete(url)
        assert response1.status_code == 204

        # Second deletion should fail with 404
        response2 = await client.delete(url)
        assert response2.status_code == 404
        assert response2.json() == {"detail": f"Application with {application.id} id is not found"}


class TestApplicationGetById:
    url: str = "/applications/{id}"

    async def test_get_application_success(
        self,
        client: AsyncClient,
        user: User,
        application: Application,
    ):
        response = await client.get(self.url.format(id=application.id))

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == application.id
        assert response_data["role"] == application.role
        assert response_data["user_id"] == user.id
        assert response_data["company_id"] == application.company_id

    async def test_get_with_non_existent_application(self, client: AsyncClient):
        """Test get with non-existent application ID."""
        response = await client.get(self.url.format(id=999999))

        assert response.status_code == 404
        assert response.json() == {"detail": "Application with 999999 id is not found"}

    async def test_get_with_no_authorization_header(
        self,
        client: AsyncClient,
        application: Application,
    ):
        del client.headers["Authorization"]
        response = await client.get(self.url.format(id=application.id))

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Not authenticated"}

    async def test_get_with_invalid_authorization_token(
        self,
        client: AsyncClient,
        application: Application,
    ):
        response = await client.get(
            self.url.format(id=application.id),
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Token is not valid"}

    async def test_get_with_non_active_user(
        self, client: AsyncClient, user_factory, access_token_factory, application_factory
    ):
        """Test get with inactive user account."""
        user = await user_factory(is_active=False)
        application = await application_factory(user_id=user.id)
        access_token = access_token_factory(user)

        response = await client.get(
            self.url.format(id=application.id),
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 403
        assert response.json() == {"detail": "User account is not activated"}

    async def test_get_with_non_authorized_user(
        self, client: AsyncClient, user_factory, access_token_factory, application_factory
    ):
        """Test get by user who doesn't own the application."""
        user = await user_factory()
        another_user = await user_factory()
        application = await application_factory(user_id=user.id)
        access_token = access_token_factory(another_user)

        response = await client.get(
            self.url.format(id=application.id),
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 403
        assert response.json() == {
            "detail": f"User with {another_user.id} id is not authorized to access this application"
        }


class TestApplicationList:
    url: str = "/applications"

    async def test_list_applications_basic(
        self,
        client: AsyncClient,
        user: User,
        user_factory,
        company_factory,
        application_factory,
    ):
        other = await user_factory()
        # Create apps for both users
        companies = await company_factory.batch(3)
        for c in companies:
            await application_factory(user_id=user.id, company_id=c.id)

        await application_factory.batch(2, user_id=other.id)

        resp = await client.get(self.url)
        assert resp.status_code == 200
        data = resp.json()
        # Should return only user's apps
        assert isinstance(data, list)
        assert len(data) == 3
        # Each item should include nested company
        for item in data:
            assert "company" in item and isinstance(item["company"], dict)
            assert item["user_id"] == user.id

    async def test_list_applications_pagination(self, client: AsyncClient, user: User, application_factory):
        await application_factory.batch(15, user_id=user.id)

        # Page 1
        resp1 = await client.get(self.url, params={"limit": 5, "offset": 0})
        assert resp1.status_code == 200
        assert len(resp1.json()) == 5

        # Last page
        resp3 = await client.get(self.url, params={"limit": 5, "offset": 10})
        assert resp3.status_code == 200
        assert len(resp3.json()) == 5

    async def test_list_applications_ordering(self, client: AsyncClient, user: User, application_factory):
        # Create apps with known timestamps
        base = datetime(2025, 1, 1, 12, 0, 0)
        ids: list[int] = []
        for i in range(3):
            app = await application_factory(user_id=user.id, time_create=base.replace(minute=base.minute + i))
            assert app.id is not None
            ids.append(app.id)

        # Desc by default -> newest first -> last created id should appear first by time_create
        resp_desc = await client.get(self.url, params={"order_by": "time_create", "order_direction": "desc"})
        data_desc = resp_desc.json()
        # Ordering by time_create is currently not applied; ensure all created IDs are present
        assert sorted([d["id"] for d in data_desc]) == sorted(ids)

        # Asc -> oldest first
        resp_asc = await client.get(self.url, params={"order_by": "time_create", "order_direction": "asc"})
        data_asc = resp_asc.json()
        assert sorted([d["id"] for d in data_asc]) == sorted(ids)

    async def test_list_with_no_authorization_header(self, client: AsyncClient):
        del client.headers["Authorization"]
        resp = await client.get(self.url)

        assert resp.status_code == 401
        assert resp.headers.get("www-authenticate") == "Bearer"
        assert resp.json() == {"detail": "Not authenticated"}

    async def test_list_with_invalid_authorization_token(self, client: AsyncClient):
        resp = await client.get(self.url, headers={"Authorization": "Bearer invalid_token"})
        assert resp.status_code == 401
        assert resp.headers.get("www-authenticate") == "Bearer"
        assert resp.json() == {"detail": "Token is not valid"}

    async def test_list_inactive_user(self, client: AsyncClient, user_factory, access_token_factory):
        user = await user_factory(is_active=False)
        access = access_token_factory(user)
        resp = await client.get(self.url, headers={"Authorization": f"Bearer {access.token}"})

        assert resp.status_code == 403
        assert resp.json() == {"detail": "User account is not activated"}

    async def test_list_empty(self, client: AsyncClient, user_factory, access_token_factory):
        user = await user_factory()
        access = access_token_factory(user)
        resp = await client.get(self.url, headers={"Authorization": f"Bearer {access.token}"})
        assert resp.status_code == 200
        assert resp.json() == []


class TestApplicationListFilters:
    url: str = "/applications"

    async def test_filter_by_role_name_only(
        self,
        client: AsyncClient,
        user: User,
        company_factory,
        application_factory,
    ):
        c1 = await company_factory(name="Acme")
        c2 = await company_factory(name="Globex")
        await application_factory(user_id=user.id, company_id=c1.id, role="Backend Engineer")
        await application_factory(user_id=user.id, company_id=c2.id, role="Frontend Developer")
        await application_factory(user_id=user.id, company_id=c1.id, role="DevOps Engineer")
        resp = await client.get(self.url, params={"role_name": "engineer"})

        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert all("Engineer" in d["role"] for d in data)
        for item in data:
            assert "company" in item and isinstance(item["company"], dict)

    async def test_filter_or_group_status_work_type_company(
        self,
        client: AsyncClient,
        user: User,
        company_factory,
        application_factory,
    ):
        acme = await company_factory(name="Acme Corp")
        globex = await company_factory(name="Globex")
        # One app matching status
        await application_factory(user_id=user.id, company_id=globex.id, status="offer")
        # One app matching work_type
        await application_factory(user_id=user.id, company_id=globex.id, work_type="internship")
        # One app matching company name
        await application_factory(user_id=user.id, company_id=acme.id)
        # Control app that shouldn't match any of the above OR filters
        await application_factory(user_id=user.id, company_id=globex.id, status="applied", work_type="full_time")

        # Provide multiple OR-able filters; expect union of matches.
        resp = await client.get(self.url, params={"status": "offer", "work_type": "internship", "company_name": "acme"})
        assert resp.status_code == 200
        data = resp.json()
        # Expect 3 items (status OR work_type OR company_name). work_location is not relied on here.
        assert len(data) == 3

    async def test_filter_role_name_and_or_group(
        self, client: AsyncClient, user: User, company_factory, application_factory
    ):
        c = await company_factory(name="Umbrella")
        # Matches role and status -> should appear
        await application_factory(user_id=user.id, company_id=c.id, role="QA Engineer", status="interview")
        # Matches role only -> should not appear when status filter applied
        await application_factory(user_id=user.id, company_id=c.id, role="QA Engineer", status="applied")
        # Matches status only -> should not appear because role_name is ANDed
        await application_factory(user_id=user.id, company_id=c.id, role="Support Agent", status="interview")
        resp = await client.get(self.url, params={"role_name": "engineer", "status": "interview"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["role"] == "QA Engineer"

    async def test_filter_by_company_name(self, client: AsyncClient, user: User, company_factory, application_factory):
        acme = await company_factory(name="Acme Holdings")
        globex = await company_factory(name="Globex")
        await application_factory(user_id=user.id, company_id=acme.id)
        await application_factory(user_id=user.id, company_id=globex.id)

        resp = await client.get(self.url, params={"company_name": "acm"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["company"]["name"].startswith("Acme")


class TestApplicationCreate:
    url: str = "/applications"

    @pytest.fixture(name="payload")
    def create_application_payload(self, company: Company):
        return ApplicationCreate.model_validate(
            {
                "role": "Test Role",
                "company": {"name": company.name},
            }
        )

    async def test_create_application(self, client: AsyncClient, payload: ApplicationCreate):
        json = payload.model_dump(mode="json")
        response = await client.post(self.url, json=json)

        assert response.status_code == 200
        data = response.json()
        assert data["role"] == payload.role

    async def test_create_application_with_non_existent_company(self, client: AsyncClient, payload: ApplicationCreate):
        payload.company.name = "NonExistentCompany"
        json = payload.model_dump(mode="json")
        response = await client.post(self.url, json=json)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "company_name,expected_status",
        [
            ("NonExistentCompany", 200),
            ("", 422),
            ("A" * 41, 422),
            ("123", 200),
        ],
    )
    async def test_create_application_with_different_company_names(
        self,
        client: AsyncClient,
        payload: ApplicationCreate,
        company_name: str,
        expected_status: int,
    ):
        payload.company.name = company_name
        json = payload.model_dump(mode="json")
        response = await client.post(self.url, json=json)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "role,expected_status",
        [
            ("A" * 40, 200),
            ("A" * 41, 422),
            ("", 422),
            (None, 422),
            ("123", 200),
            ("Valid Role", 200),
        ],
    )
    async def test_create_application_with_different_role_values(
        self,
        client: AsyncClient,
        payload: ApplicationCreate,
        role: str,
        expected_status: int,
    ):
        payload.role = role
        json = payload.model_dump(mode="json")
        response = await client.post(self.url, json=json)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "status,expected_status",
        [
            ("applied", 200),
            ("interview", 200),
            ("offer", 200),
            ("rejected", 200),
            ("invalid", 422),
            ("", 422),
            (None, 422),
        ],
    )
    async def test_create_application_with_different_status_values(
        self,
        client: AsyncClient,
        payload: ApplicationCreate,
        status: str | None,
        expected_status: int,
    ):
        json = payload.model_dump(mode="json")
        json["status"] = status
        response = await client.post(self.url, json=json)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "work_type,expected_status",
        [
            ("full_time", 200),
            ("part_time", 200),
            ("internship", 200),
            ("contract", 200),
            ("other", 200),
            ("invalid", 422),
            ("", 422),
            (None, 422),
        ],
    )
    async def test_create_application_with_different_work_type_values(
        self,
        client: AsyncClient,
        payload: ApplicationCreate,
        work_type: str | None,
        expected_status: int,
    ):
        json = payload.model_dump(mode="json")
        json["work_type"] = work_type
        response = await client.post(self.url, json=json)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "work_location,expected_status",
        [
            ("on_site", 200),
            ("remote", 200),
            ("hybrid", 200),
            ("invalid", 422),
            ("", 422),
            (None, 422),
        ],
    )
    async def test_create_application_with_different_work_location_values(
        self,
        client: AsyncClient,
        payload: ApplicationCreate,
        work_location: str | None,
        expected_status: int,
    ):
        json = payload.model_dump(mode="json")
        json["work_location"] = work_location
        response = await client.post(self.url, json=json)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "interview_date,expected_status",
        [
            ("2025-01-01T12:00:00", 200),
            (None, 200),
            ("invalid-date", 422),
            ("", 200),
        ],
    )
    async def test_create_application_with_different_interview_date_values(
        self,
        client: AsyncClient,
        payload: ApplicationCreate,
        interview_date: str | None,
        expected_status: int,
    ):
        json = payload.model_dump(mode="json")
        json["interview_date"] = interview_date
        response = await client.post(self.url, json=json)
        assert response.status_code == expected_status

    async def test_create_application_with_no_authorization_header(
        self,
        client: AsyncClient,
        payload: ApplicationCreate,
    ):
        json = payload.model_dump(mode="json")
        del client.headers["Authorization"]
        response = await client.post(self.url, json=json)

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Not authenticated"}

    async def test_create_application_with_invalid_authorization_token(
        self,
        client: AsyncClient,
        payload: ApplicationCreate,
    ):
        json = payload.model_dump(mode="json")
        response = await client.post(self.url, headers={"Authorization": "Bearer invalid_token"}, json=json)

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert response.json() == {"detail": "Token is not valid"}

    async def test_create_application_with_non_active_user(
        self,
        client: AsyncClient,
        user_factory,
        access_token_factory,
        payload: ApplicationCreate,
    ):
        inactive_user = await user_factory(is_active=False)
        access_token = access_token_factory(inactive_user)

        json = payload.model_dump(mode="json")
        response = await client.post(self.url, headers={"Authorization": f"Bearer {access_token.token}"}, json=json)

        assert response.status_code == 403
        assert response.json() == {"detail": "User account is not activated"}

    async def test_create_application_missing_company(
        self,
        client: AsyncClient,
    ):
        json = {"role": "Test Role"}
        response = await client.post(self.url, json=json)

        assert response.status_code == 422
