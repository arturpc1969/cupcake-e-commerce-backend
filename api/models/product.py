from django.db import models
import uuid

from api.models.common import BaseModel, ActiveManager


class Product(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    promotion = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
