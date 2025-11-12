from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from ninja import Router
from ninja.errors import ValidationError as NinjaValidationError

from accounts.schemas import SignupSchema, TokenPairResponse, LoginSchema, RefreshSchema, ErrorResponse
from accounts.utils import create_access_token, create_refresh_token, decode_token

router = Router(tags=["auth"])
User = get_user_model()


# --- Routes ---
@router.post("/signup")
def signup(request, data: SignupSchema):
    if User.objects.filter(username=data.username).exists():
        return {"error": "User already exists"}
    user = User(
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        cpf=data.cpf,
    )
    user.set_password(data.password)
    try:
        user.full_clean()
        user.save()
        return {"message": "User successfully created", "uuid": user.uuid}
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)


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
