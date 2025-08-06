from datetime import datetime, timedelta, timezone

from freezegun import freeze_time
from httpx import AsyncClient

from app import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.domain import User

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
        assert response.json() == {"detail": "User does not exist"}

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


class TestUserChangePassword(BaseTest):
    async def test_change_password_success(self, client: AsyncClient):
        """Test successful password change with valid access token and correct old password."""
        user = await self.create_user(is_active=True)
        assert user.id is not None
        access_token = self.create_access_token(user)
        old_password = self.get_user_password()
        new_password = "NewTestPass123"

        form_data = {
            "old_password": old_password,
            "new_password": new_password,
            "confirm_new_password": new_password,
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {access_token.token}"},
            data=form_data,
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Password changed successfully"}

        # Verify password was actually changed in database
        updated_user = await self.get_user(user.id)
        assert updated_user is not None
        assert self.password_hasher.verify(new_password, updated_user.password)
        assert not self.password_hasher.verify(old_password, updated_user.password)

    async def test_change_password_with_invalid_access_token(self, client: AsyncClient):
        """Test password change with invalid access token."""
        invalid_token = "invalid.token.here"
        form_data = {
            "old_password": "OldPass123",
            "new_password": "NewPass123",
            "confirm_new_password": "NewPass123",
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {invalid_token}"},
            data=form_data,
        )

        assert response.status_code == 400
        assert "Invalid access token" in response.json()["detail"]

    async def test_change_password_with_expired_access_token(self, client: AsyncClient):
        """Test password change with expired access token."""
        user = await self.create_user(is_active=True)
        assert user.id is not None
        access_token = self.create_access_token(user)

        form_data = {
            "old_password": self.get_user_password(),
            "new_password": "NewPass123",
            "confirm_new_password": "NewPass123",
        }

        with freeze_time(datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES + 1)):
            response = await client.patch(
                "/users/change-password",
                headers={"Authorization": f"Bearer {access_token.token}"},
                data=form_data,
            )

        assert response.status_code == 400
        assert "Invalid access token" in response.json()["detail"]

    async def test_change_password_with_missing_access_token(self, client: AsyncClient):
        """Test password change without access token."""
        form_data = {
            "old_password": "OldPass123",
            "new_password": "NewPass123",
            "confirm_new_password": "NewPass123",
        }

        response = await client.patch("/users/change-password", data=form_data)

        assert response.status_code == 401

    async def test_change_password_with_incorrect_old_password(self, client: AsyncClient):
        """Test password change with incorrect old password."""
        user = await self.create_user(is_active=True)
        assert user.id is not None
        access_token = self.create_access_token(user)
        wrong_old_password = "WrongOldPass123"
        new_password = "NewTestPass123"

        form_data = {
            "old_password": wrong_old_password,
            "new_password": new_password,
            "confirm_new_password": new_password,
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {access_token.token}"},
            data=form_data,
        )

        assert response.status_code == 400
        assert "Old password is incorrect" in response.json()["detail"]

        # Verify password was not changed
        updated_user = await self.get_user(user.id)
        assert updated_user is not None
        assert self.password_hasher.verify(self.get_user_password(), updated_user.password)

    async def test_change_password_with_non_existent_user(self, client: AsyncClient):
        """Test password change with access token for non-existent user."""

        non_existent_email = "nonexistent@example.com"
        non_existent_id = 99999
        user = User(id=non_existent_id, email=non_existent_email, password="OldPass123")
        token = self.create_access_token(user)

        form_data = {
            "old_password": "OldPass123",
            "new_password": "NewPass123",
            "confirm_new_password": "NewPass123",
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {token.token}"},
            data=form_data,
        )

        assert response.status_code == 404
        assert "User does not exist" in response.json()["detail"]

    async def test_change_password_with_mismatched_confirmation(self, client: AsyncClient):
        """Test password change when new password and confirmation don't match."""
        user = await self.create_user(is_active=True)
        assert user.id is not None
        access_token = self.create_access_token(user)
        old_password = self.get_user_password()

        form_data = {
            "old_password": old_password,
            "new_password": "NewPass123",
            "confirm_new_password": "DifferentPass123",
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {access_token.token}"},
            data=form_data,
        )

        assert response.status_code == 422
        response_data = response.json()
        assert any("New password and confirmation do not match" in str(error) for error in response_data["detail"])

    async def test_change_password_with_missing_form_fields(self, client: AsyncClient):
        """Test password change with missing required form fields."""
        user = await self.create_user(is_active=True)
        access_token = self.create_access_token(user)

        # Test missing old_password
        form_data = {
            "new_password": "NewPass123",
            "confirm_new_password": "NewPass123",
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {access_token.token}"},
            data=form_data,
        )

        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["type"] == "missing"
        assert "old_password" in response_data["detail"][0]["loc"]

    async def test_change_password_with_empty_form_fields(self, client: AsyncClient):
        """Test password change with empty form fields."""
        user = await self.create_user(is_active=True)
        access_token = self.create_access_token(user)

        form_data = {
            "old_password": "",
            "new_password": "",
            "confirm_new_password": "",
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {access_token.token}"},
            data=form_data,
        )

        assert response.status_code == 422
        response_data = response.json()
        # Should have validation errors for password requirements
        assert len(response_data["detail"]) > 0

    async def test_change_password_with_weak_new_password(self, client: AsyncClient):
        """Test password change with weak new password."""
        user = await self.create_user(is_active=True)
        assert user.id is not None
        access_token = self.create_access_token(user)
        old_password = self.get_user_password()
        weak_password = "123"  # Too short and weak

        form_data = {
            "old_password": old_password,
            "new_password": weak_password,
            "confirm_new_password": weak_password,
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {access_token.token}"},
            data=form_data,
        )

        assert response.status_code == 422
        response_data = response.json()
        # Should have validation errors for password requirements
        assert len(response_data["detail"]) > 0

    async def test_change_password_with_wrong_token_type(self, client: AsyncClient):
        """Test password change with verification token instead of access token."""
        user = await self.create_user(is_active=True)
        verification_token = self.create_verification_token(user)

        form_data = {
            "old_password": self.get_user_password(),
            "new_password": "NewPass123",
            "confirm_new_password": "NewPass123",
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {verification_token}"},
            data=form_data,
        )

        assert response.status_code == 400
        assert "Invalid access token" in response.json()["detail"]

    async def test_change_password_with_inactive_user(self, client: AsyncClient):
        """Test password change for inactive user."""
        user = await self.create_user(is_active=False)
        assert user.id is not None
        access_token = self.create_access_token(user)
        old_password = self.get_user_password()

        form_data = {
            "old_password": old_password,
            "new_password": "NewPass123",
            "confirm_new_password": "NewPass123",
        }

        response = await client.patch(
            "/users/change-password",
            headers={"Authorization": f"Bearer {access_token.token}"},
            data=form_data,
        )

        # Should work regardless of user activation status
        assert response.status_code == 200
        assert response.json() == {"message": "Password changed successfully"}

    async def test_change_password_concurrent_requests(self, client: AsyncClient):
        """Test multiple simultaneous password change requests."""
        user = await self.create_user(is_active=True)
        assert user.id is not None
        access_token = self.create_access_token(user)
        old_password = self.get_user_password()

        form_data = {
            "old_password": old_password,
            "new_password": "NewPass123",
            "confirm_new_password": "NewPass123",
        }

        # Make two concurrent requests
        import asyncio

        async def make_request():
            return await client.patch(
                "/users/change-password",
                headers={"Authorization": f"Bearer {access_token.token}"},
                data=form_data,
            )

        responses = await asyncio.gather(make_request(), make_request())

        # One should succeed, one might fail due to password mismatch
        # (if the first one completes before the second one starts)
        success_count = sum(1 for r in responses if r.status_code == 200)
        assert success_count >= 1
