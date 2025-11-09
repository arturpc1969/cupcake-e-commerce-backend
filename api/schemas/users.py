from ninja import Schema
from uuid import UUID

from pydantic import field_serializer


# Response Schema (simplified)
class UserOut(Schema):
    uuid: UUID
    username: str
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    cpf: str | None = None
    email: str | None = None
    is_staff: bool

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
