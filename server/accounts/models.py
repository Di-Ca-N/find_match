from django.db import models
from django.contrib.auth.models import AbstractUser
from localflavor.br.models import BRCPFField


class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, unique=True)
    cpf = BRCPFField(null=True, unique=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"User: {self.username}"
