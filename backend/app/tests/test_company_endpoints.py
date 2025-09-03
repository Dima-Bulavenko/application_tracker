from httpx import AsyncClient

from .base import BaseTest


class TestCompanyGetById(BaseTest):
    async def test_get_company_success(self, client: AsyncClient):
        """Should return company by id with 200 status."""
        company = await self.create_company()
        assert company.id is not None

        response = await client.get(f"/companies/{company.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == company.id
        assert data["name"] == company.name

    async def test_get_company_not_found(self, client: AsyncClient):
        """Should return 404 for non-existent company id."""
        response = await client.get("/companies/999999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Company not found"}


class TestGetUserCompanies(BaseTest):
    async def test_without_access_token(self, client: AsyncClient):
        response = await client.get("/companies/user")
        assert response.status_code == 401

    async def test_returns_companies_for_user(self, client: AsyncClient):
        user = await self.create_user()
        token = self.create_access_token(user)

        # Two companies, one app each for this user
        c1 = await self.create_company(name="Acme Alpha")
        c2 = await self.create_company(name="Beta Corp")
        await self.create_application(user_id=user.id, company_id=c1.id)
        await self.create_application(user_id=user.id, company_id=c2.id)

        response = await client.get(
            "/companies/user",
            headers={"Authorization": f"Bearer {token.token}"},
        )
        assert response.status_code == 200
        data = response.json()
        names = [c["name"] for c in data]
        assert set(names) == {"Acme Alpha", "Beta Corp"}

    async def test_filters_by_name_contains_case_insensitive(self, client: AsyncClient):
        user = await self.create_user()
        token = self.create_access_token(user)

        c1 = await self.create_company(name="Globex Corporation")
        c2 = await self.create_company(name="Initech")
        c3 = await self.create_company(name="GLOBE Solutions")
        # Link apps for user
        await self.create_application(user_id=user.id, company_id=c1.id)
        await self.create_application(user_id=user.id, company_id=c2.id)
        await self.create_application(user_id=user.id, company_id=c3.id)

        response = await client.get(
            "/companies/user",
            params={"name_contains": "globe"},
            headers={"Authorization": f"Bearer {token.token}"},
        )

        assert response.status_code == 200
        names = [c["name"] for c in response.json()]
        assert set(names) == {"Globex Corporation", "GLOBE Solutions"}

    async def test_deduplicates_companies_when_multiple_apps(self, client: AsyncClient):
        user = await self.create_user()
        token = self.create_access_token(user)

        c = await self.create_company(name="Duplicate Inc")
        # Two applications for the same company and user
        await self.create_application(user_id=user.id, company_id=c.id, role="Role 1")
        await self.create_application(user_id=user.id, company_id=c.id, role="Role 2")

        response = await client.get(
            "/companies/user",
            headers={"Authorization": f"Bearer {token.token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Duplicate Inc"

    async def test_pagination_and_sorting(self, client: AsyncClient):
        user = await self.create_user()
        token = self.create_access_token(user)

        # create several companies
        names = ["C", "A", "B", "D"]
        companies = [await self.create_company(name=n) for n in names]
        for c in companies:
            await self.create_application(user_id=user.id, company_id=c.id)

        # order by name asc, limit 2, offset 1
        response = await client.get(
            "/companies/user",
            params={"order_by": "name", "order_direction": "asc", "limit": 2, "offset": 1},
            headers={"Authorization": f"Bearer {token.token}"},
        )

        assert response.status_code == 200
        data = response.json()
        # Sorted names would be [A, B, C, D] -> slice [1:3] => [B, C]
        assert [c["name"] for c in data] == ["B", "C"]
