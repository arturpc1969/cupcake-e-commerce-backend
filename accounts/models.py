from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # extra field (optional)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username
