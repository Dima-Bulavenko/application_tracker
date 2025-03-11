from enum import Enum

from decouple import Csv, config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int)
DEBUG = config("DEBUG", cast=bool)
TOKEN_TYPE = "bearer"
ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", cast=Csv())


class Tags(Enum):
    USER = "user"
    APPLICATION = "application"
    COMPANY = "company"
