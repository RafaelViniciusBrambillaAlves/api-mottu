from datetime import datetime, timedelta
from jose import jwt
from os import getenv

SECRET_KEY = getenv("JWT_SECRET_KEY")
ALGORITHM = getenv("JWT_ALGORITHM")

ACCESS_TOKEN_EXPIRES_MINUTES = int(getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 15))
REFRESH_TOKEN_EXPIRES_DAYS = int(getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 7))

if not SECRET_KEY or not ALGORITHM:
    raise RuntimeError("Jwt configuration is missing")

ISSUER = "mottu-api"

def create_access_token(user_id: int, role: str) -> str:
    now = datetime.utcnow()

    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "iss": ISSUER,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)).timestamp())
    }

    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    now = datetime.utcnow()
    
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iss": ISSUER,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS)).timestamp())
    }

    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

def decode_token(token: str):
    return jwt.decode(
        token, 
        SECRET_KEY, 
        algorithms = [ALGORITHM],
        issuer = ISSUER
    )
