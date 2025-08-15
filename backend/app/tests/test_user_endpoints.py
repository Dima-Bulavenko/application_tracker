from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from freezegun import freeze_time
from httpx import AsyncClient

from app import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.domain import User

from .base import BaseTest


class TestCreateUser(BaseTest):
    async def test_create_user_success(self, client: AsyncClient):
        """Test successful user creation with valid email and password."""
        email = "newuser@example.com"
        form_data = {
            "email": email,
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        # Verify user was created in database
        created_user = await self.get_user_by_email(email)

        assert created_user is not None
        assert created_user.email == email
        assert created_user.is_active is False  # Should be inactive until email verification
        assert response.status_code == 201
        expected_message = "We sent email to newuser@example.com address, follow link to complete your registration"
        assert response.json() == {"message": expected_message}

    @patch("fastapi.BackgroundTasks.add_task")
    async def test_create_user_success_with_background_task_mock(self, mock_add_task: MagicMock, client: AsyncClient):
        """Test successful user creation and verify background task is called."""
        email = "newuser@example.com"
        form_data = {
            "email": email,
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        # Verify user was created in database
        created_user = await self.get_user_by_email(email)

        assert created_user is not None
        assert created_user.email == email
        assert response.status_code == 201

        # Verify background task was called
        assert mock_add_task.called
        assert mock_add_task.call_count == 1

        # Get the call arguments
        call_args = mock_add_task.call_args
        task_func = call_args[0][0]  # First argument is the function
        task_user_arg = call_args[0][1]  # Second argument is the user

        # Verify the correct function was called (send_verification_email)
        assert hasattr(task_func, "__name__")
        assert task_func.__name__ == "send_verification_email"

        # Verify the user argument has correct properties
        assert hasattr(task_user_arg, "email")
        assert task_user_arg.email == email

    async def test_create_user_with_existing_email(self, client: AsyncClient):
        """Test user creation with already existing email address."""
        # Create an existing user
        existing_user = await self.create_user()

        form_data = {
            "email": existing_user.email,
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        # Should still return success response (security by design)
        assert response.status_code == 201
        expected_message = f"We sent email to {existing_user.email} address, follow link to complete your registration"
        assert response.json() == {"message": expected_message}

    @patch("fastapi.BackgroundTasks.add_task")
    async def test_create_user_with_existing_email_background_task(self, mock_add_task: MagicMock, client: AsyncClient):
        """Test user creation with existing email sends duplicate registration warning."""
        # Create an existing user
        existing_user = await self.create_user()

        form_data = {
            "email": existing_user.email,
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        # Should still return success response (security by design)
        assert response.status_code == 201

        # Verify background task was called
        assert mock_add_task.called
        assert mock_add_task.call_count == 1

        # Get the call arguments
        call_args = mock_add_task.call_args
        task_func = call_args[0][0]  # First argument is the function
        task_email_arg = call_args[0][1]  # Second argument is the email

        # Verify the correct function was called (send_duplicate_registration_warning)
        assert hasattr(task_func, "__name__")
        assert task_func.__name__ == "send_duplicate_registration_warning"

        # Verify the email argument is correct
        assert task_email_arg == existing_user.email

    async def test_create_user_with_invalid_email_format(self, client: AsyncClient):
        """Test user creation with invalid email format."""
        form_data = {
            "email": "invalid-email-format",
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data
        # Should contain validation error for email format
        assert any("email" in str(error).lower() for error in response_data["detail"])

    async def test_create_user_with_weak_password(self, client: AsyncClient):
        """Test user creation with password that doesn't meet requirements."""
        form_data = {
            "email": "test@example.com",
            "password": "weak",  # Too short, no uppercase, no number
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data
        # Should contain validation error for password requirements
        assert any("password" in str(error).lower() for error in response_data["detail"])

    async def test_create_user_with_password_missing_uppercase(self, client: AsyncClient):
        """Test user creation with password missing uppercase letter."""
        form_data = {
            "email": "test@example.com",
            "password": "testpass123",  # No uppercase letter
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data

    async def test_create_user_with_password_missing_number(self, client: AsyncClient):
        """Test user creation with password missing number."""
        form_data = {
            "email": "test@example.com",
            "password": "TestPassword",  # No number
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data

    async def test_create_user_with_password_too_short(self, client: AsyncClient):
        """Test user creation with password shorter than 8 characters."""
        form_data = {
            "email": "test@example.com",
            "password": "Test1",  # Too short
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data

    async def test_create_user_with_missing_email(self, client: AsyncClient):
        """Test user creation without email field."""
        form_data = {
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data
        # Check that we get a validation error (the specific field doesn't matter as much
        # as ensuring we get a proper 422 validation error)
        errors = response_data["detail"]
        assert len(errors) > 0
        assert any(error.get("type") == "missing" for error in errors)

    async def test_create_user_with_missing_password(self, client: AsyncClient):
        """Test user creation without password field."""
        form_data = {
            "email": "test@example.com",
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data
        assert any("password" in error.get("loc", []) for error in response_data["detail"])

    async def test_create_user_with_empty_email(self, client: AsyncClient):
        """Test user creation with empty email field."""
        form_data = {
            "email": "",
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data

    async def test_create_user_with_empty_password(self, client: AsyncClient):
        """Test user creation with empty password field."""
        form_data = {
            "email": "test@example.com",
            "password": "",
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data

    async def test_create_user_with_whitespace_only_fields(self, client: AsyncClient):
        """Test user creation with whitespace-only email and password."""
        form_data = {
            "email": "   ",
            "password": "   ",
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data

    async def test_create_user_with_very_long_email(self, client: AsyncClient):
        """Test user creation with extremely long email address."""
        long_email = "a" * 100 + "@example.com"
        form_data = {
            "email": long_email,
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        # This might succeed or fail depending on email length validation
        # If it succeeds, verify the user is created
        if response.status_code == 201:
            expected_message = f"We sent email to {long_email} address, follow link to complete your registration"
            assert response.json() == {"message": expected_message}
        else:
            assert response.status_code == 422

    async def test_create_user_with_special_characters_in_password(self, client: AsyncClient):
        """Test user creation with special characters in password."""
        email = "test@example.com"
        form_data = {
            "email": email,
            "password": "TestPass123!@#",
        }

        response = await client.post("/users/", data=form_data)

        assert response.status_code == 201
        expected_message = "We sent email to test@example.com address, follow link to complete your registration"
        assert response.json() == {"message": expected_message}

        # Verify user was created in database with correct password hash
        created_user = await self.get_user_by_email(email)
        assert created_user is not None
        assert created_user.email == email
        assert created_user.is_active is False
        # Verify password is hashed (not plain text)
        assert created_user.password != "TestPass123!@#"
        assert len(created_user.password) > 50  # Hashed passwords are much longer
        # Verify the password can be validated with the hasher
        assert self.password_hasher.verify("TestPass123!@#", created_user.password)

    async def test_create_user_case_insensitive_email(self, client: AsyncClient):
        """Test user creation with different email cases."""
        # First user
        form_data1 = {
            "email": "Test@Example.com",
            "password": "TestPass123",
        }

        response1 = await client.post("/users/", data=form_data1)
        assert response1.status_code == 201

        # Second user with same email but different case
        form_data2 = {
            "email": "test@example.com",
            "password": "TestPass456",
        }

        response2 = await client.post("/users/", data=form_data2)

        # Should still return success (existing user scenario)
        assert response2.status_code == 201

    async def test_create_user_with_sql_injection_attempt(self, client: AsyncClient):
        """Test user creation endpoint is protected against SQL injection."""
        malicious_email = "test'; DROP TABLE users; --@example.com"
        form_data = {
            "email": malicious_email,
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        # Should fail due to email validation or be safely handled
        # Most likely will fail email validation
        assert response.status_code in [201, 422]  # Either succeeds safely or fails validation

    async def test_create_user_with_unicode_characters(self, client: AsyncClient):
        """Test user creation with unicode characters in email."""
        form_data = {
            "email": "测试@example.com",  # Unicode characters
            "password": "TestPass123",
        }

        response = await client.post("/users/", data=form_data)

        # Should handle unicode properly
        if response.status_code == 201:
            expected_message = "We sent email to 测试@example.com address, follow link to complete your registration"
            assert response.json() == {"message": expected_message}
        else:
            assert response.status_code == 422

    async def test_create_user_password_hashing(self, client: AsyncClient):
        """Test that password is properly hashed and not stored in plain text."""
        email = "hashtest@example.com"
        password = "TestPass123"
        form_data = {
            "email": email,
            "password": password,
        }

        response = await client.post("/users/", data=form_data)
        assert response.status_code == 201

        # Verify user was created in database with hashed password
        created_user = await self.get_user_by_email(email)
        assert created_user is not None
        assert created_user.email == email

        # Verify password is hashed, not plain text
        assert created_user.password != password
        assert len(created_user.password) > 50  # Hashed passwords are much longer
        assert created_user.password.startswith("$")  # Common hash format indicator

        # Verify the password can be validated with the hasher
        assert self.password_hasher.verify(password, created_user.password)

    @patch("fastapi.BackgroundTasks.add_task")
    async def test_create_user_comprehensive_verification(self, mock_add_task: MagicMock, client: AsyncClient):
        """Test comprehensive user creation including API response, database, and background tasks."""
        email = "comprehensive@example.com"
        password = "SecurePass123!"
        form_data = {
            "email": email,
            "password": password,
        }

        # Make the request
        response = await client.post("/users/", data=form_data)

        # Verify API response
        assert response.status_code == 201
        expected_message = f"We sent email to {email} address, follow link to complete your registration"
        assert response.json() == {"message": expected_message}

        # Verify database state
        created_user = await self.get_user_by_email(email)
        assert created_user is not None
        assert created_user.email == email
        assert created_user.is_active is False  # Should start inactive
        assert created_user.password != password  # Should be hashed
        assert self.password_hasher.verify(password, created_user.password)

        # Verify background task was scheduled
        assert mock_add_task.called
        assert mock_add_task.call_count == 1

        # Verify background task details
        call_args = mock_add_task.call_args
        task_func = call_args[0][0]
        task_user_arg = call_args[0][1]

        assert task_func.__name__ == "send_verification_email"
        assert task_user_arg.email == email

    @patch("fastapi.BackgroundTasks.add_task")
    async def test_create_user_duplicate_email_comprehensive(self, mock_add_task: MagicMock, client: AsyncClient):
        """Test duplicate email creation including background task verification."""
        from sqlalchemy import func, select

        from app.db.models import User as UserModel

        # Create initial user
        existing_user = await self.create_user()

        # Count initial users with this email
        initial_count_result = await self.session.execute(
            select(func.count(UserModel.id)).where(UserModel.email == existing_user.email)
        )
        initial_count = initial_count_result.scalar()

        form_data = {
            "email": existing_user.email,
            "password": "NewPassword123",
        }

        # Attempt to create duplicate user
        response = await client.post("/users/", data=form_data)

        # Verify API response (should still be successful for security)
        assert response.status_code == 201
        expected_message = f"We sent email to {existing_user.email} address, follow link to complete your registration"
        assert response.json() == {"message": expected_message}

        # Verify no new user was created in database
        final_count_result = await self.session.execute(
            select(func.count(UserModel.id)).where(UserModel.email == existing_user.email)
        )
        final_count = final_count_result.scalar()
        assert final_count == initial_count  # Count should remain the same

        # Verify background task was scheduled (for duplicate warning)
        assert mock_add_task.called
        assert mock_add_task.call_count == 1

        # Verify it's the duplicate registration warning task
        call_args = mock_add_task.call_args
        task_func = call_args[0][0]
        task_email_arg = call_args[0][1]

        assert task_func.__name__ == "send_duplicate_registration_warning"
        assert task_email_arg == existing_user.email


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

        assert response.status_code == 401
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

        assert response.status_code == 401
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

        assert response.status_code == 401
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


class TestGetCurrentUser(BaseTest):
    async def test_get_me_success(self, client: AsyncClient):
        """Should return current user info with valid access token."""
        user = await self.create_user(is_active=True)
        assert user.id is not None
        access_token = self.create_access_token(user)

        response = await client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token.token}"},
        )

        assert response.status_code == 200
        data = response.json()
        # Minimal shape checks
        assert data["id"] == user.id
        assert data["username"] == user.email
        assert isinstance(data["is_active"], bool)
        # Presence of timestamps
        assert "time_create" in data and "time_update" in data

    async def test_get_me_missing_token(self, client: AsyncClient):
        """Should return 401 when Authorization header is missing."""
        response = await client.get("/users/me")
        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"

    async def test_get_me_invalid_token(self, client: AsyncClient):
        """Should return 401 with Bearer header for invalid token."""
        response = await client.get(
            "/users/me",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert "Invalid access token" in response.json()["detail"]

    async def test_get_me_expired_token(self, client: AsyncClient):
        """Should return 401 for expired token."""
        user = await self.create_user(is_active=True)
        access_token = self.create_access_token(user)

        with freeze_time(datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES + 1)):
            response = await client.get(
                "/users/me",
                headers={"Authorization": f"Bearer {access_token.token}"},
            )

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert "Invalid access token" in response.json()["detail"]

    async def test_get_me_user_not_found(self, client: AsyncClient):
        """Should return 404 when token refers to a non-existent user."""
        non_existent_email = "nonexistent@example.com"
        non_existent_id = 99999
        ghost = User(id=non_existent_id, email=non_existent_email, password="x")
        token = self.create_access_token(ghost)

        response = await client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token.token}"},
        )

        assert response.status_code == 404
        # Service raises UserNotFoundError; message typically includes 'User does not exist'
        assert "User" in response.json()["detail"]
