import os
import secrets
from datetime import timedelta

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

settings = Settings()