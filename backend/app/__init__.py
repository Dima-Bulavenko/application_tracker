from enum import Enum

from environs import env

env.read_env(override=True)

SECRET_KEY = env.str("SECRET_KEY")
ALGORITHM = env.str("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", 5)
REFRESH_TOKEN_EXPIRE_MINUTES = env.int("REFRESH_TOKEN_EXPIRE_MINUTES", 160)
VERIFICATION_TOKEN_EXPIRE_MINUTES = env.int("VERIFICATION_TOKEN_EXPIRE_MINUTES", 1440)
RESEND_ACTIVATION_COOLDOWN_MINUTES = env.int("RESEND_ACTIVATION_COOLDOWN_MINUTES", 2)
DEBUG = env.bool("DEBUG", False)
TOKEN_TYPE = "bearer"
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", subcast=str)
ALLOWED_ORIGINS = env.list("ALLOWED_ORIGINS", subcast=str)
FRONTEND_ORIGIN = env.str("FRONTEND_ORIGIN")

# OAuth Configuration
GOOGLE_CLIENT_ID = env.str("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = env.str("GOOGLE_CLIENT_SECRET", "")
OAUTH_REDIRECT_URI = env.str("OAUTH_REDIRECT_URI", "http://localhost:5173/oauth")


class Tags(Enum):
    USER = "user"
    APPLICATION = "application"
    COMPANY = "company"
    AUTHENTICATION = "authentication"
