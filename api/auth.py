from datetime import datetime, timedelta, UTC

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from ninja import Router, Schema

router = Router()
User = get_user_model()

# use the Django SECRET_KEY
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


# --- Schemas ---
class SignupSchema(Schema):
    username: str
    first_name: str
    last_name: str
    password: str
    email: str
    cpf: str | None = None


class LoginSchema(Schema):
    username: str
    password: str


class TokenPairResponse(Schema):
    access: str
    refresh: str


class RefreshSchema(Schema):
    refresh: str


class ErrorResponse(Schema):
    error: str


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


# --- Routes ---
@router.post("/signup")
def signup(request, data: SignupSchema):
    if User.objects.filter(username=data.username).exists():
        return {"error": "User already exists"}
    user = User.objects.create_user(
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=data.password,
        cpf=data.cpf,
    )
    return {"message": "User successfully created", "id": user.id}


@router.post("/login", response={200: TokenPairResponse, 401: ErrorResponse})
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return 401, {"error": "Invalid credentials"}
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    return 200, {"access": access, "refresh": refresh}


@router.post("/refresh", response={200: TokenPairResponse, 401: ErrorResponse})
def refresh_token(request, data: RefreshSchema):
    payload = decode_token(data.refresh)
    if not payload or payload.get("type") != "refresh":
        return 401, {"error": "Invalid refresh token"}
    user_id = payload["user_id"]
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)  # optional: generate new refresh
    return 200, {"access": access, "refresh": refresh}
