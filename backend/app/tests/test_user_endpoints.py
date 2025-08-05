from datetime import datetime, timedelta, timezone

from httpx import AsyncClient

from .base import BaseTest


class TestUserActivation(BaseTest):
    async def test_activate_user_success(self, client: AsyncClient):
        """Test successful user activation with valid token."""
        user = await self.create_user(is_active=False)
        assert user.id is not None
        token = self.create_verification_token(user)

        response = await client.patch(f"/users/activate?token={token}")

        assert response.status_code == 200
        assert response.json() == {"message": "Account activated successfully"}

        # Verify user is actually activated in database
        updated_user = await self.get_user(user.id)
        assert updated_user is not None
        assert updated_user.is_active is True

    async def test_activate_with_invalid_token(self, client: AsyncClient):
        """Test activation with malformed or invalid token."""
        invalid_token = "invalid.token.here"

        response = await client.patch(f"/users/activate?token={invalid_token}")

        assert response.status_code == 400
        assert "Invalid activation token" in response.json()["detail"]

    async def test_activate_with_expired_token(self, client: AsyncClient):
        """Test activation with expired verification token."""
        user = await self.create_user(is_active=False)
        assert user.id is not None
        expired_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        token = self.create_verification_token_for_user_data(user.email, user.id, exp=expired_time)

        response = await client.patch(f"/users/activate?token={token}")

        assert response.status_code == 400
        assert "Invalid activation token" in response.json()["detail"]

    async def test_activate_with_non_existent_user(self, client: AsyncClient):
        """Test activation with token for non-existent user."""
        non_existent_email = "nonexistent@example.com"
        non_existent_id = 99999
        token = self.create_verification_token_for_user_data(non_existent_email, non_existent_id)

        response = await client.patch(f"/users/activate?token={token}")

        assert response.status_code == 404
        assert response.json() == {"detail": f"User with email = {non_existent_email}"}

    async def test_activate_already_active_user(self, client: AsyncClient):
        """Test activation of user who is already activated."""
        user = await self.create_user(is_active=True)
        assert user.id is not None
        token = self.create_verification_token(user)

        response = await client.patch(f"/users/activate?token={token}")

        assert response.status_code == 409
        assert response.json() == {"detail": "User is already activated"}

    async def test_activate_with_missing_token(self, client: AsyncClient):
        """Test activation without providing token parameter."""
        response = await client.patch("/users/activate")

        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["type"] == "missing"
        assert "token" in response_data["detail"][0]["loc"]

    async def test_activate_with_empty_token(self, client: AsyncClient):
        """Test activation with empty token parameter."""
        response = await client.patch("/users/activate?token=")

        assert response.status_code == 400
        assert "Invalid activation token" in response.json()["detail"]

    async def test_activate_with_wrong_token_type(self, client: AsyncClient):
        """Test activation with access token instead of verification token."""
        user = await self.create_user(is_active=False)
        access_token = self.create_access_token(user)

        response = await client.patch(f"/users/activate?token={access_token.token}")

        assert response.status_code == 400
        assert "Invalid activation token" in response.json()["detail"]

    async def test_activate_with_token_for_different_user(self, client: AsyncClient):
        """Test activation with token created for different user."""
        user1 = await self.create_user(is_active=False)
        user2 = await self.create_user(is_active=False)
        assert user1.id is not None
        assert user2.id is not None

        # Create token for user2 but try to activate user1's account
        token = self.create_verification_token(user2)

        response = await client.patch(f"/users/activate?token={token}")

        # This should succeed for user2, not user1
        assert response.status_code == 200

        # Verify user1 is still inactive and user2 is now active
        updated_user1 = await self.get_user(user1.id)
        updated_user2 = await self.get_user(user2.id)
        assert updated_user1 is not None
        assert updated_user2 is not None
        assert updated_user1.is_active is False
        assert updated_user2.is_active is True

    async def test_activate_multiple_times_with_same_token(self, client: AsyncClient):
        """Test that same token cannot be used multiple times."""
        user = await self.create_user(is_active=False)
        assert user.id is not None
        token = self.create_verification_token(user)

        # First activation should succeed
        response1 = await client.patch(f"/users/activate?token={token}")
        assert response1.status_code == 200

        # Second activation with same token should fail
        response2 = await client.patch(f"/users/activate?token={token}")
        assert response2.status_code == 409
        assert response2.json() == {"detail": "User is already activated"}

    async def test_activate_with_sql_injection_attempt(self, client: AsyncClient):
        """Test activation endpoint is protected against SQL injection."""
        malicious_token = "'; DROP TABLE users; --"

        response = await client.patch(f"/users/activate?token={malicious_token}")

        assert response.status_code == 400
        assert "Invalid activation token" in response.json()["detail"]
