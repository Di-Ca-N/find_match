from django.db import models
from django.contrib.auth.models import AbstractUser
from localflavor.br.models import BRCPFField


class User(AbstractUser):
    cpf = BRCPFField(null=True)
