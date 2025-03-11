from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated

import jwt
from fastapi import Cookie, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    ALLOWED_HOSTS,
    DEBUG,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    TOKEN_TYPE,
)
from app.routers import application, company, user
from app.schemas import (
    Token,
)
from app.utils import create_token

from .db import create_db_tables
from .dependencies import AuthenticatedUserDep


@asynccontextmanager
async def lifespan(_):
    await create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(application.router)
app.include_router(company.router)


@app.post("/login")
async def login(user: AuthenticatedUserDep, response: Response):
    payload = {"sub": user.email, "type": "access"}
    access_token = create_token(payload, ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update(type="refresh")
    refresh_token = create_token(payload, REFRESH_TOKEN_EXPIRE_MINUTES)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not DEBUG,
        max_age=int(REFRESH_TOKEN_EXPIRE_MINUTES * 60),
        path="/refresh",
    )
    return Token(access_token=access_token, token_type=TOKEN_TYPE)


@app.get("/refresh")
async def refresh(
    response: Response, refresh_token: Annotated[str | None, Cookie()] = None
):
    try:
        payload: dict = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"required": ["exp"]},
        )
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Token expires, log in again",
            {"WWW-Authenticate": "Bearer"},
        ) from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Could not authorize user",
            {"WWW-Authenticate": "Bearer"},
        ) from err

    new_access_token = create_token(payload, ACCESS_TOKEN_EXPIRE_MINUTES)
    new_refresh_token = create_token(payload, REFRESH_TOKEN_EXPIRE_MINUTES)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=not DEBUG,
        max_age=int(REFRESH_TOKEN_EXPIRE_MINUTES * 60),
        path="/refresh",
    )
    return Token(access_token=new_access_token, token_type=TOKEN_TYPE)
