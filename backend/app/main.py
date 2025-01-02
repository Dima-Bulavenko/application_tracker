from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    ApplicationCreateDTO,
    ApplicationReadRelDTO,
    CompanyReadDTO,
)

from .db import create_db_tables
from .dependencies import SessionDep
from .orm import ApplicationORM, CompanyORM

origins = [
    "http://localhost:3000",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
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


@app.post("/applications/", response_model=ApplicationReadRelDTO)
def create_application(new_app: ApplicationCreateDTO, session: SessionDep):
    app = ApplicationORM.create_app(new_app, session)
    session.commit()
    print(app)
    return app


@app.get("/applications/", response_model=list[ApplicationReadRelDTO])
def get_application(session: SessionDep):
    return ApplicationORM.get_apps(session)


@app.get("/companies/", response_model=list[CompanyReadDTO])
def get_companies(session: SessionDep):
    return CompanyORM.get_companies(session)
