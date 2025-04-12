from enum import Enum

from environs import env

env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
ALGORITHM = env.str("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", 5)
REFRESH_TOKEN_EXPIRE_MINUTES = env.int("REFRESH_TOKEN_EXPIRE_MINUTES", 160)
DEBUG = env.bool("DEBUG", False)
TOKEN_TYPE = "bearer"
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", subcast=str)


class Tags(Enum):
    USER = "user"
    APPLICATION = "application"
    COMPANY = "company"
