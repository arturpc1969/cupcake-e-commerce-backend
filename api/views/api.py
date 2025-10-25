from ninja import NinjaAPI

from accounts.views import auth
from . import users, products, deliveryaddresses, orders, orderitems

api = NinjaAPI()


api.add_router("/auth/", auth.router)
api.add_router("/users/", users.router)
api.add_router("/products/", products.router)
api.add_router("/orders/", orders.router)
api.add_router("/order-items/", orderitems.router)
api.add_router("/delivery-addresses/", deliveryaddresses.router)
