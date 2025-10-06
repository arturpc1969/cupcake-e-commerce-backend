from uuid import UUID

from ninja import Schema


class DeliveryAddressIn(Schema):
    address_name: str
    address_description: str
    city: str
    state: str
    zip_code: str


class DeliveryAddressOut(Schema):
    uuid: UUID
    address_name: str
    address_description: str
    city: str
    state: str
    zip_code: str
