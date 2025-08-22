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
