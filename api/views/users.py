import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from ninja import Router, Schema
from pydantic import field_serializer

from api.deps import AuthBearer  # your authentication via token

User = get_user_model()
router = Router(tags=["users"], auth=AuthBearer())


# Response Schema (simplified)
class UserOut(Schema):
    uuid: uuid.UUID
    username: str
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    cpf: str | None = None
    email: str | None = None

    @field_serializer("full_name")
    def get_full_name(self, value, info):
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return None


# Update Schema
class UserUpdate(Schema):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    cpf: str | None = None
    email: str | None = None


# Deactivate Schema
class UserDeactivate(Schema):
    is_active: bool = False


class ChangePasswordIn(Schema):
    old_password: str
    new_password: str


@router.get("/me", response=UserOut)
def get_me(request):
    """Return the data of authenticated user"""
    return request.auth  # request.auth is the user coming from AuthBearer


@router.put("/me", response=UserOut)
def update_me(request, data: UserUpdate):
    """Update the data of authenticated user"""
    user = request.auth
    for field, value in data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    user.save()
    return user


@router.patch("/me")
def deactivate_me(request, data: UserDeactivate):
    """Deactivate the authenticated user"""
    user = request.auth
    if data.is_active:
        return {'message': 'Nothing changed, user remains active'}
    user.is_active = data.is_active
    user.save()
    return {'message': 'User successfully deactivated'}


@router.delete("/me", response={204: None})
def delete_me(request):
    """Delete the authenticated user"""
    user = request.auth
    user.delete()
    return 204, None


@router.post("/change-password")
def change_password(request, data: ChangePasswordIn):
    """
    Allow the user to change their password
    Necessary to provide the current and new passwords
    """
    user = request.auth

    if not check_password(data.old_password, user.password):
        return {"success": False, "message": "Current password incorrect"}

    user.set_password(data.new_password)
    user.save()
    return {"success": True, "message": "Password changed successfully"}
