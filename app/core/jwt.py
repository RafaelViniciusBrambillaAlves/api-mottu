from datetime import datetime, timedelta
from jose import jwt
from os import getenv

SECRET_KEY = getenv("JWT_SECRET_KEY")
ALGORITHM = getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRES_MINUTES = int(getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES"))
REFRESH_TOKEN_EXPIRES_DAYS = int(getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS"))

def create_access_token(subject: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRES_MINUTES)

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access",
        "iss": "fastapi-app"
    }

    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

def create_refresh_token(subject: dict) -> str:
    expire = datetime.utcnow() + timedelta(days = REFRESH_TOKEN_EXPIRES_DAYS)
    
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "refresh"
    }

    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

