from ninja import Schema


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
