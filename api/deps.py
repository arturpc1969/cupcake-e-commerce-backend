from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from ninja.security import HttpBearer

from .auth import decode_token

User = get_user_model()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return None
        try:
            return User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            return None


auth = AuthBearer()
