from fastapi import APIRouter

from app import Tags

router = APIRouter(prefix="/applications", tags=[Tags.APPLICATION])
