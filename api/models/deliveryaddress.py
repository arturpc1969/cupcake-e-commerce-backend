import uuid

from django.conf import settings
from django.db import models

from api.models.common import BaseModel, ActiveManager


class DeliveryAddress(BaseModel):

    class StatesAcronym(models.TextChoices):
        AC = 'AC', 'Acre'
        AL = 'AL', 'Alagoas'
        AM = 'AM', 'Amazonas'
        AP = 'AP', 'Amapá'
        BA = 'BA', 'Bahia'
        CE = 'CE', 'Ceará'
        DF = 'DF', 'Distrito Federal'
        ES = 'ES', 'Espírito Santo'
        GO = 'GO', 'Goiás'
        MA = 'MA', 'Maranhão'
        MG = 'MG', 'Minas Gerais'
        MS = 'MS', 'Mato Grosso do Sul'
        MT = 'MT', 'Mato Grosso'
        PA = 'PA', 'Pará'
        PB = 'PB', 'Paraíba'
        PE = 'PE', 'Pernambuco'
        PI = 'PI', 'Piauí'
        PR = 'PR', 'Paraná'
        RJ = 'RJ', 'Rio de Janeiro'
        RN = 'RN', 'Rio Grande do Norte'
        RO = 'RO', 'Rondônia'
        RR = 'RR', 'Roraima'
        RS = 'RS', 'Rio Grande do Sul'
        SC = 'SC', 'Santa Catarina'
        SE = 'SE', 'Sergipe'
        SP = 'SP', 'São Paulo'
        TO = 'TO', 'Tocantins'

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    address_name = models.CharField(max_length=100)
    address_description = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=StatesAcronym.choices)
    zip_code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="delivery_addresses")

    objects = ActiveManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.address_name}, {self.address_description} - {self.city}/{self.state}"
