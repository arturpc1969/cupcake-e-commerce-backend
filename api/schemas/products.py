import uuid
from typing import Optional

from ninja import Schema


class ProductOut(Schema):
    uuid: uuid.UUID
    name: str
    description: str
    price: float
    promotion: bool
    image: Optional[str] = None

    @staticmethod
    def resolve_image(obj):
        """Retorna a URL completa da imagem do Cloudinary"""
        if obj.image:
            return obj.image.url  # Cloudinary retorna URL completa automaticamente
        return None
