from enum import Enum

from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
TOKEN_TYPE = "bearer"


class Tags(Enum):
    USER = "user"
    APPLICATION = "application"
    COMPANY = "company"
