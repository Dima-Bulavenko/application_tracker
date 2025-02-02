from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound

from .db.models import Application, Base, Company, User
from .schemas import ApplicationCreate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

TAlchemyModel = TypeVar("TAlchemyModel", bound=Base)


class BaseORM[TAlchemyModel]:
    model: TAlchemyModel

    def __init__(self, session: AsyncSession):
        self.session = session


class ApplicationORM(BaseORM):
    model: Application

    async def create(self, app_data: ApplicationCreate, user: User) -> Application:
        interview_date = app_data.interview_date
        app_data_dict = app_data.model_dump(mode="json", exclude={"interview_date"})
        company_dict = app_data_dict.pop("company")
        company = await get_or_create(
            Company,
            self.session,
            create_with_values=company_dict,
            name=company_dict["name"],
        )
        application = Application(**app_data_dict, company=company)
        application.user = user

        # This needed because asyncpg don't accept data and time in string format
        application.interview_date = interview_date
        self.session.add(application)
        await self.session.commit()
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


class UserORM(BaseORM):  # TEST: UserORM
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
