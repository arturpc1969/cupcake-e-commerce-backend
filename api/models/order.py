from django.conf import settings
from django.db import models
import uuid

from api.models import DeliveryAddress
from api.models.common import BaseModel


class Order(BaseModel):

    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'CREDIT_CARD', 'Cartão de Crédito'
        DEBIT_CARD = 'DEBIT_CARD', 'Cartão de Débito'
        BANK_SLIP = 'BANK_SLIP', 'Boleto Bancário'
        PIX = 'PIX', 'Pix'
        CASH = 'CASH', 'Dinheiro'

    class OrderStatus(models.TextChoices):
        RECEIVED = 'RECEIVED', 'Pedido Recebido'
        PREPARATION = 'PREPARATION', 'Pedido em Preparação'
        DELIVERY = 'DELIVERY', 'Pedido em Entrega'
        WAITING_PAYMENT = 'WAITING_PAYMENT', 'Aguardando Pagamento'
        DELIVERED = 'DELIVERED', 'Pedido Entregue'
        FINISHED = 'FINISHED', 'Pedido Finalizado'
        CANCELED = 'CANCELED', 'Pedido Cancelado'

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_number = models.PositiveBigIntegerField(unique=True, editable=False)
    order_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=25, choices=PaymentMethod.choices)
    status = models.CharField(max_length=25, choices=OrderStatus.choices, default=OrderStatus.RECEIVED)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="my_orders")
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            super().save(*args, **kwargs)
            self.order_number = self.id
            return super().save(update_fields=["order_number"])
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order number {self.order_number} - Status {self.status}"
