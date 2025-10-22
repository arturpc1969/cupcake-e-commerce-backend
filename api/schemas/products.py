import uuid
from typing import Optional

from ninja import Schema


class ProductOut(Schema):
    uuid: uuid.UUID
    name: str
    description: str
    price: float
    image: Optional[str] = None
