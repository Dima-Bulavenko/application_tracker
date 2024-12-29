from __future__ import annotations

from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from .db.models import Application, Base, Company
from .schemas import ApplicationCreateDTO

TAlchemyModel = TypeVar("TAlchemyModel", bound=Base)


class ApplicationORM:
    @staticmethod
    def create_app(new_app: ApplicationCreateDTO, session: Session) -> Application:
        new_app_dict = new_app.model_dump(mode="json")
        company_dict = new_app_dict.pop("company")
        company = get_or_create(
            Company, session, default=company_dict, name=company_dict["name"]
        )
        application = Application(**new_app_dict, company=company)
        session.add(application)
        session.commit()
        return application

    @staticmethod
    def get_apps(session: Session):
        res = session.scalars(select(Application))
        return res


class CompanyORM:
    @staticmethod
    def get_companies(session: Session):
        companies = session.scalars(select(Company))
        return companies


def get_or_create(
    model: type[TAlchemyModel],
    session: Session,
    default: dict | None = None,
    **kwargs,
):
    """Search and return an instance based on kwargs.

    If no instance is found try to create a new one.

    Args:
        model (DeclarativeBase): Class of a model that should be created.
        session (Session): Data base session.
        default (dict | None, optional): Parameters to create new model. Defaults to None.
        **kwargs: Parameters to look the instance by.
    """
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        kwargs.update(default)
        instance = model(**kwargs)
        session.add(instance)
    return instance
