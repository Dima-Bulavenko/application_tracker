from app.core.domain import User
from app.core.dto import AccessTokenPayload, UserChangePassword, UserCreate, UserRead, VerificationTokenPayload
from app.core.exceptions import InvalidPasswordError, UserAlreadyActivatedError, UserNotFoundError
from app.core.repositories import IUserRepository
from app.core.security import IPasswordHasher, ITokenStrategy


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        verification_strategy: ITokenStrategy[VerificationTokenPayload],
        access_token_strategy: ITokenStrategy[AccessTokenPayload],
    ) -> None:
        self.user_repo = user_repo
        self.verification_strategy = verification_strategy
        self.access_token_strategy = access_token_strategy
        self.password_hasher = password_hasher

    async def create(self, user_data: UserCreate) -> UserRead:
        user_data.password = self.password_hasher.hash(user_data.password)
        user = await self.user_repo.save(User(user_data.email, user_data.password))
        return UserRead.model_validate(user, from_attributes=True)

    async def get_by_email(self, email: str) -> UserRead:
        user = await self.user_repo.get_by_email(email)
        return UserRead.model_validate(user, from_attributes=True)

    async def activate_with_token(self, token: str) -> UserRead:
        token_object = self.verification_strategy.verify_token(token)
        user = await self.user_repo.get_by_email(token_object.payload.user_email)

        # FIXME: user.id check only for typechecking, refactor User domain to fix it
        if not user or user.id is None:
            raise UserNotFoundError("User does not exist")

        if user.is_active:
            raise UserAlreadyActivatedError("User is already activated")

        updated_user = await self.user_repo.update(user.id, is_active=True)
        return UserRead.model_validate(updated_user, from_attributes=True)

    async def change_password_with_token(self, access_token: str, passwords: UserChangePassword) -> UserRead:
        access_token_object = self.access_token_strategy.verify_token(access_token)

        user = await self.user_repo.get_by_email(access_token_object.payload.user_email)
        # FIXME: user.id check only for typechecking, refactor User domain to fix it
        if user is None or user.id is None:
            raise UserNotFoundError("User does not exist")

        if not self.password_hasher.verify(passwords.old_password, user.password):
            raise InvalidPasswordError("Old password is incorrect")

        new_hashed_password = self.password_hasher.hash(passwords.new_password)
        updated_user = await self.user_repo.update(user.id, password=new_hashed_password)
        return UserRead.model_validate(updated_user, from_attributes=True)
