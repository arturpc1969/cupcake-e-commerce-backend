from django.contrib.auth import get_user_model
from ninja.security import HttpBearer

from accounts.utils import decode_token

User = get_user_model()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return None
        try:
            user = User.objects.get(id=payload["user_id"])
            if not user.is_active:
                return None
            return user
        except User.DoesNotExist:
            return None


auth = AuthBearer()
