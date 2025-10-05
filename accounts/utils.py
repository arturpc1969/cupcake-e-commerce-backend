import jwt
from django.conf import settings
from datetime import datetime, timedelta, UTC

# use the Django SECRET_KEY
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


# --- Utility functions ---
def create_access_token(user_id: int):
    payload = {
        "user_id": user_id,
        "type": "access",
        "exp": datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES),
        "iat": datetime.now(UTC),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: int):
    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_LIFETIME_DAYS),
        "iat": datetime.now(UTC),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
