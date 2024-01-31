from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from localflavor.br.models import BRCPFField


class User(AbstractUser):
    username = models.CharField(
        max_length=150, null=True, unique=True, verbose_name=_("username")
    )
    cpf = BRCPFField(null=True, unique=True, verbose_name="CPF")
    isOrganizer = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    def __str__(self):
        return f"User: {self.username}"
    
class OrganizerRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('accepted', 'Aceito'),
        ('declined', 'Recusado'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Pedido para virar organizador de {self.user.username}"