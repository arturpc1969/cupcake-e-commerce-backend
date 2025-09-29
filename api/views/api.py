from ninja import NinjaAPI

from api import auth
from . import protected

api = NinjaAPI()


api.add_router("/auth/", auth.router)
api.add_router("/protected/", protected.router)
