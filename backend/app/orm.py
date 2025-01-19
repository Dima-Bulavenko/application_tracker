from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, TypeVar

from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound

from .db.models import Application, Base, Company, User
from .schemas import ApplicationCreate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.schemas import UserInDB

TAlchemyModel = TypeVar("TAlchemyModel", bound=Base)


class BaseORM[TAlchemyModel]:
    model: TAlchemyModel

    def __init__(self, session: AsyncSession):
        self.session = session


class ApplicationORM:
    @staticmethod
    async def create_app(
        new_app: ApplicationCreate, session: AsyncSession, user: UserInDB
    ) -> Application:
        new_app_dict = new_app.model_dump(mode="json")
        company_dict = new_app_dict.pop("company")
        company = await get_or_create(
            Company, session, create_with_values=company_dict, name=company_dict["name"]
        )
        # FIXME: Come up with caching user
        users = await session.scalars(select(User).filter_by(email=user.email))
        user_instance = users.one()
        # FIXME: The asyncpg takes only datetime data type so I need to convert back to datetime
        # there's must be a better way https://github.com/MagicStack/asyncpg/issues/692?utm_source=chatgpt.com
        new_app_dict["interview_date"] = datetime.fromisoformat(
            new_app_dict["interview_date"]
        )

        application = Application(**new_app_dict, company=company)
        application.user = user_instance
        session.add(application)
        await session.commit()
        return application

    @staticmethod
    async def get_apps(session: AsyncSession):
        res = await session.scalars(select(Application))
        return res


class CompanyORM:
    @staticmethod
    async def get_companies(session: AsyncSession):
        companies = await session.scalars(select(Company))
        return companies


class UserORM(BaseORM):
    model: type[User] = User

    async def get(self, **kwargs):
        users = select(self.model).filter_by(**kwargs)
        user_scalars = await self.session.scalars(users)
        return user_scalars.one()

    async def create(self, email: str, password: str, **kwargs):
        user = self.model(email=email, password=password, **kwargs)
        self.session.add(user)
        await self.session.commit()
        return user


async def get_or_create(
    model: type[TAlchemyModel],
    session: AsyncSession,
    create_with_values: dict[str, Any],
    **search_by,
):  # TEST: get_or_create func
    """Try to look for database entry using "search_by" dict.
    If there is only one DB entry return it.

    If no instance is found update "search_by" dict with "create_with_values" and create and add new entry to "session".

    If more then one entry found raise MultipleResultsFound.

    Args:
        model (type[TAlchemyModel]): Class of a model that should be found or created.
        session (AsyncSession): Data base session.
        search_by (dict[str, Any]): Params to look a DB entry for.
        **create_with_values: Params to create an new DB entry if there is no found.
    """
    try:
        query = select(model).filter_by(**search_by)
        item = await session.scalars(query)
        return item.one()
    except NoResultFound:
        search_by.update(create_with_values)
        instance = model(**search_by)
        session.add(instance)
    return instance
