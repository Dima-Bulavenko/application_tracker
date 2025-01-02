from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from .db import Session as SessionMaker


def get_session() -> Session:
    with SessionMaker() as session:
        yield session
        session.commit()


SessionDep = Annotated[Session, Depends(get_session)]
