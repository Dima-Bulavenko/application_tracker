from fastapi import APIRouter

from app import Tags

router = APIRouter(prefix="/companies", tags=[Tags.COMPANY])
