from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.routing import APIRoute
from mangum import Mangum

from app import ALLOWED_HOSTS
from app.routers import application, auth, company, oauth, user


def custom_generate_unique_id(route: APIRoute):
    return f"{route.name}"


app = FastAPI(generate_unique_id_function=custom_generate_unique_id, root_path="/api/v1")

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=ALLOWED_HOSTS,
)


@app.get("/health", tags=["health"], include_in_schema=False)
async def test_endpoint():
    return {"message": "The backend is running."}


app.include_router(user.router)
app.include_router(application.router)
app.include_router(company.router)
app.include_router(auth.router)
app.include_router(oauth.router)

handler = Mangum(app)
