from datetime import date
from uuid import UUID

from ninja import Schema

from api.schemas.deliveryaddresses import DeliveryAddressOut
from api.schemas.products import ProductOut


class OrderItemIn(Schema):
    order_uuid: UUID
    product_uuid: UUID
    quantity: int


class ItemOut(ProductOut):
    quantity: int


class OrderItemOut(Schema):
    order_uuid: UUID
    order_number: int
    order_date: date
    payment_method: str
    status: str
    delivery_address: DeliveryAddressOut
    products: list[ItemOut]
