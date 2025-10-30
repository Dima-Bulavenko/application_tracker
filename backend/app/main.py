from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from mangum import Mangum

from app import ALLOWED_HOSTS
from app.routers import application, auth, company, user

from .db import create_db_tables


@asynccontextmanager
async def lifespan(_):
    await create_db_tables()
    yield


def custom_generate_unique_id(route: APIRoute):
    return f"{route.name}"


app = FastAPI(lifespan=lifespan, generate_unique_id_function=custom_generate_unique_id)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"], include_in_schema=False)
async def test_endpoint():
    return {"message": "The backend is running."}


app.include_router(user.router)
app.include_router(application.router)
app.include_router(company.router)
app.include_router(auth.router)

handler = Mangum(app)
