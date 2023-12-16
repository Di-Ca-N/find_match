from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from localflavor.br.models import BRCPFField


class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, unique=True, verbose_name=_("username"))
    cpf = BRCPFField(null=True, unique=True, verbose_name="CPF")

    USERNAME_FIELD = "username"

    def __str__(self):
        return f"User: {self.username}"
