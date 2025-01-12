from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import ACCESS_TOKEN_EXPIRE_MINUTES, TOKEN_TYPE
from app.routers import application, company, user
from app.schemas import (
    Token,
)
from app.utils import authenticate_user, create_access_token

from .db import create_db_tables
from .dependencies import LoginFormDep, SessionDep

origins = [
    "http://localhost:3000",
]


@asynccontextmanager
async def lifespan(_):
    create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(application.router)
app.include_router(company.router)


@app.post("/login")
async def login(form_data: LoginFormDep, session: SessionDep):
    user = await authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type=TOKEN_TYPE)
