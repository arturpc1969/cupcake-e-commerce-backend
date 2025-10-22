from datetime import date
from uuid import UUID

from ninja import Schema

from api.schemas.deliveryaddresses import DeliveryAddressOut
from api.schemas.users import UserOut


class OrderIn(Schema):
    payment_method: str
    delivery_address_uuid: UUID


class OrderOut(Schema):
    uuid: UUID
    order_number: int
    order_date: date
    payment_method: str
    status: str
    delivery_address: DeliveryAddressOut


class OrderAdminOut(Schema):
    uuid: UUID
    order_number: int
    order_date: date
    payment_method: str
    status: str
    delivery_address: DeliveryAddressOut
    user: UserOut
