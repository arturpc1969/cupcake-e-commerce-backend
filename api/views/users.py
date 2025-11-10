from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from ninja import Router
from ninja.errors import ValidationError as NinjaValidationError

from accounts.deps import AuthBearer  # your authentication via token
from api.schemas.users import UserOut, UserUpdate, UserDeactivate, ChangePasswordIn

User = get_user_model()
router = Router(tags=["users"], auth=AuthBearer())


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
    try:
        user.full_clean()
        user.save()
        return user
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)


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


@router.post("/me/change-password")
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
