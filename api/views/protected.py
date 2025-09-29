from ninja import Router

from api.deps import auth

router = Router(auth=auth)

@router.get("/me")
def me(request):
    user = request.auth
    return {"id": user.id, "username": user.username, "email": user.email}
