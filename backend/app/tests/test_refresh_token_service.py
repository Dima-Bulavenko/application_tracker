"""Tests for refresh token rotation, revocation, and reuse detection."""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import pytest
from freezegun import freeze_time

from app import REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app.core.exceptions import (
    RefreshTokenReuseError,
    RefreshTokenRevokedError,
    TokenExpireError,
    TokenInvalidError,
)
from app.core.services.refresh_token_service import RefreshTokenService
from app.tests.base import BaseTest


class TestRefreshTokenService(BaseTest):
    """Test refresh token service functionality."""

    def _hash_token(self, raw_token: str) -> str:
        """Helper to hash a token."""
        return hmac.new(SECRET_KEY.encode(), raw_token.encode(), hashlib.sha256).hexdigest()

    async def test_issue_token(self):
        """Test issuing a new refresh token."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        raw_token = await service.issue(user.id)

        assert raw_token is not None
        assert len(raw_token) > 0

        # Verify token is stored in database
        token_hash = self._hash_token(raw_token)
        token = await self.refresh_token_repo.get_by_hash(token_hash)
        assert token is not None
        assert token.user_id == user.id
        assert token.family_id is not None
        assert token.parent_token_id is None
        assert not token.is_revoked()
        assert not token.is_used()

    async def test_issue_token_with_parent(self):
        """Test issuing a token with a parent (token family)."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        # Issue first token (root)
        first_token = await service.issue(user.id)
        first_token_hash = self._hash_token(first_token)
        first_token_obj = await self.refresh_token_repo.get_by_hash(first_token_hash)

        # Issue second token with same family_id and parent
        second_token = await service.issue(
            user.id, family_id=first_token_obj.family_id, parent_token_id=first_token_obj.id
        )
        second_token_hash = self._hash_token(second_token)
        second_token_obj = await self.refresh_token_repo.get_by_hash(second_token_hash)

        assert second_token_obj.parent_token_id == first_token_obj.id
        assert second_token_obj.family_id == first_token_obj.family_id

    async def test_validate_and_rotate_success(self):
        """Test successful token validation and rotation."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        # Issue initial token
        old_token = await service.issue(user.id)
        old_token_hash = self._hash_token(old_token)

        # Validate and rotate
        new_token, returned_user_id = await service.validate_and_rotate(old_token, user.id)

        assert new_token != old_token
        assert returned_user_id == user.id

        # Verify old token is marked as used
        old_token_obj = await self.refresh_token_repo.get_by_hash(old_token_hash)
        assert old_token_obj.is_used()

        # Verify new token is valid and has old token as parent
        new_token_hash = self._hash_token(new_token)
        new_token_obj = await self.refresh_token_repo.get_by_hash(new_token_hash)
        assert new_token_obj.is_valid()
        assert new_token_obj.parent_token_id == old_token_obj.id

    async def test_validate_and_rotate_token_not_found(self):
        """Test validation fails for non-existent token."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        fake_token = secrets.token_urlsafe(32)

        with pytest.raises(TokenInvalidError, match="Token is not valid"):
            await service.validate_and_rotate(fake_token, user.id)

    async def test_validate_and_rotate_wrong_user(self):
        """Test validation fails when token doesn't belong to user."""
        user1 = await self.create_user()
        user2 = await self.create_user(email="another@example.com")
        service = RefreshTokenService(self.refresh_token_repo)

        # Issue token for user1
        token = await service.issue(user1.id)

        # Try to use it with user2's ID
        with pytest.raises(TokenInvalidError, match="Token does not belong to the specified user"):
            await service.validate_and_rotate(token, user2.id)

    async def test_validate_and_rotate_expired_token(self):
        """Test validation fails for expired token."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        # Issue token
        token = await service.issue(user.id)

        # Fast forward past expiration
        with freeze_time(datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES + 1)):
            with pytest.raises(TokenExpireError, match="Token is expired"):
                await service.validate_and_rotate(token, user.id)

    async def test_validate_and_rotate_revoked_token(self):
        """Test validation fails for revoked token."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        # Issue and revoke token
        token = await service.issue(user.id)
        await service.revoke(token)

        with pytest.raises(RefreshTokenRevokedError, match="Token has been revoked"):
            await service.validate_and_rotate(token, user.id)

    async def test_token_reuse_detection(self):
        """Test that reusing a token triggers token family revocation."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        # Issue and rotate token once
        token1 = await service.issue(user.id)
        token2, _ = await service.validate_and_rotate(token1, user.id)

        # Try to reuse token1 (should trigger family revocation)
        with pytest.raises(RefreshTokenReuseError, match="Token has already been used"):
            await service.validate_and_rotate(token1, user.id)

        # Verify both tokens in the family are revoked
        token1_hash = self._hash_token(token1)
        token2_hash = self._hash_token(token2)

        token1_obj = await self.refresh_token_repo.get_by_hash(token1_hash)
        token2_obj = await self.refresh_token_repo.get_by_hash(token2_hash)

        # Both should be revoked (same family_id)
        assert token1_obj.is_revoked()
        assert token2_obj.is_revoked()
        assert token1_obj.family_id == token2_obj.family_id

    async def test_revoke_single_token(self):
        """Test revoking a single token."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        token = await service.issue(user.id)
        await service.revoke(token)

        token_hash = self._hash_token(token)
        token_obj = await self.refresh_token_repo.get_by_hash(token_hash)
        assert token_obj.is_revoked()

    async def test_revoke_all_for_user(self):
        """Test revoking all tokens for a user."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        # Issue multiple tokens
        token1 = await service.issue(user.id)
        token2 = await service.issue(user.id)
        token3 = await service.issue(user.id)

        # Revoke all
        await service.revoke_all_for_user(user.id)

        # Verify all are revoked
        for token in [token1, token2, token3]:
            token_hash = self._hash_token(token)
            token_obj = await self.refresh_token_repo.get_by_hash(token_hash)
            assert token_obj.is_revoked()

    async def test_revoke_all_does_not_affect_other_users(self):
        """Test that revoking all tokens for one user doesn't affect others."""
        user1 = await self.create_user()
        user2 = await self.create_user(email="user2@example.com")
        service = RefreshTokenService(self.refresh_token_repo)

        # Issue tokens for both users
        user1_token = await service.issue(user1.id)
        user2_token = await service.issue(user2.id)

        # Revoke all for user1
        await service.revoke_all_for_user(user1.id)

        # Verify user1's token is revoked
        user1_token_hash = self._hash_token(user1_token)
        user1_token_obj = await self.refresh_token_repo.get_by_hash(user1_token_hash)
        assert user1_token_obj.is_revoked()

        # Verify user2's token is still valid
        user2_token_hash = self._hash_token(user2_token)
        user2_token_obj = await self.refresh_token_repo.get_by_hash(user2_token_hash)
        assert not user2_token_obj.is_revoked()

    async def test_token_rotation_chain(self):
        """Test multiple token rotations create a proper chain."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        # Create a chain of rotations
        token1 = await service.issue(user.id)
        token2, _ = await service.validate_and_rotate(token1, user.id)
        token3, _ = await service.validate_and_rotate(token2, user.id)

        # Verify the chain
        token1_hash = self._hash_token(token1)
        token2_hash = self._hash_token(token2)
        token3_hash = self._hash_token(token3)

        token1_obj = await self.refresh_token_repo.get_by_hash(token1_hash)
        token2_obj = await self.refresh_token_repo.get_by_hash(token2_hash)
        token3_obj = await self.refresh_token_repo.get_by_hash(token3_hash)

        # Verify family_id is the same for all tokens
        assert token1_obj.family_id == token2_obj.family_id == token3_obj.family_id

        # Verify chain structure
        assert token1_obj.parent_token_id is None
        assert token2_obj.parent_token_id == token1_obj.id
        assert token3_obj.parent_token_id == token2_obj.id

        # Verify used status
        assert token1_obj.is_used()
        assert token2_obj.is_used()
        assert not token3_obj.is_used()

    async def test_custom_expiration(self):
        """Test issuing token with custom expiration."""
        user = await self.create_user()
        service = RefreshTokenService(self.refresh_token_repo)

        custom_expiration = datetime.now(timezone.utc) + timedelta(minutes=10)
        token = await service.issue(user.id, expires_at=custom_expiration)

        token_hash = self._hash_token(token)
        token_obj = await self.refresh_token_repo.get_by_hash(token_hash)

        # Allow for small time differences (within 1 second)
        assert abs((token_obj.expires_at - custom_expiration).total_seconds()) < 1
