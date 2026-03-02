from httpx import AsyncClient


class TestCompanyGetById:
    url: str = "/companies/{id}"

    async def test_get_company_success(self, client: AsyncClient, company_factory):
        """Should return company by id with 200 status."""
        company = await company_factory()
        assert company.id is not None

        response = await client.get(self.url.format(id=company.id))

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == company.id
        assert data["name"] == company.name

    async def test_get_company_not_found(self, client: AsyncClient):
        """Should return 404 for non-existent company id."""
        response = await client.get(self.url.format(id=999999))

        assert response.status_code == 404
        assert response.json() == {"detail": "Company not found"}


class TestGetUserCompanies:
    url: str = "/companies/user"

    async def test_without_access_token(self, client: AsyncClient):
        response = await client.get(self.url)
        assert response.status_code == 401

    async def test_returns_companies_for_user(
        self,
        client: AsyncClient,
        user_factory,
        access_token_factory,
        company_factory,
        application_factory,
    ):
        user = await user_factory()
        token = access_token_factory(user)

        # Two companies, one app each for this user
        c1 = await company_factory(name="Acme Alpha")
        c2 = await company_factory(name="Beta Corp")
        await application_factory(user_id=user.id, company_id=c1.id)
        await application_factory(user_id=user.id, company_id=c2.id)

        response = await client.get(
            self.url,
            headers={"Authorization": f"Bearer {token.token}"},
        )
        assert response.status_code == 200
        data = response.json()
        names = [c["name"] for c in data]
        assert set(names) == {"Acme Alpha", "Beta Corp"}

    async def test_filters_by_name_contains_case_insensitive(
        self,
        client: AsyncClient,
        user_factory,
        access_token_factory,
        company_factory,
        application_factory,
    ):
        user = await user_factory()
        token = access_token_factory(user)

        c1 = await company_factory(name="Globex Corporation")
        c2 = await company_factory(name="Initech")
        c3 = await company_factory(name="GLOBE Solutions")
        # Link apps for user
        await application_factory(user_id=user.id, company_id=c1.id)
        await application_factory(user_id=user.id, company_id=c2.id)
        await application_factory(user_id=user.id, company_id=c3.id)

        response = await client.get(
            self.url,
            params={"name_contains": "globe"},
            headers={"Authorization": f"Bearer {token.token}"},
        )

        assert response.status_code == 200
        names = [c["name"] for c in response.json()]
        assert set(names) == {"Globex Corporation", "GLOBE Solutions"}

    async def test_deduplicates_companies_when_multiple_apps(
        self,
        client: AsyncClient,
        user_factory,
        access_token_factory,
        company_factory,
        application_factory,
    ):
        user = await user_factory()
        token = access_token_factory(user)

        c = await company_factory(name="Duplicate Inc")
        # Two applications for the same company and user
        await application_factory(user_id=user.id, company_id=c.id, role="Role 1")
        await application_factory(user_id=user.id, company_id=c.id, role="Role 2")

        response = await client.get(
            self.url,
            headers={"Authorization": f"Bearer {token.token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Duplicate Inc"

    async def test_pagination_and_sorting(
        self,
        client: AsyncClient,
        user_factory,
        access_token_factory,
        company_factory,
        application_factory,
    ):
        user = await user_factory()
        token = access_token_factory(user)

        # create several companies
        names = ["C", "A", "B", "D"]
        companies = [await company_factory(name=n) for n in names]
        for c in companies:
            await application_factory(user_id=user.id, company_id=c.id)

        # order by name asc, limit 2, offset 1
        response = await client.get(
            self.url,
            params={"order_by": "name", "order_direction": "asc", "limit": 2, "offset": 1},
            headers={"Authorization": f"Bearer {token.token}"},
        )

        assert response.status_code == 200
        data = response.json()
        # Sorted names would be [A, B, C, D] -> slice [1:3] => [B, C]
        assert [c["name"] for c in data] == ["B", "C"]
