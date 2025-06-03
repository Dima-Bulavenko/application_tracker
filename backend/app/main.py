from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import ALLOWED_HOSTS
from app.routers import application, auth, company, user

from .db import create_db_tables


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
app.include_router(auth.router)
