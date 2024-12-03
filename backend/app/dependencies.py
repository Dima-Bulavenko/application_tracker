from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from .db import Session as SessionMaker


def get_session():
    with SessionMaker() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
