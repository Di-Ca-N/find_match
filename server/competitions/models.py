from django.db import models
from localflavor.br.models import BRStateField
from django.urls import reverse

from accounts.models import User
from sports.models import Modality


class Competition(models.Model):
    organizer = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Organizador"
    )
    modality = models.ForeignKey(
        Modality, on_delete=models.PROTECT, verbose_name="Modalidade"
    )
    title = models.CharField(max_length=50, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    datetime = models.DateTimeField(verbose_name="Data e Horário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    city = models.CharField(max_length=80, verbose_name="Cidade")
    state = BRStateField(verbose_name="Estado")
    address = models.CharField(max_length=100, verbose_name="Endereço")
    image = models.ImageField(
        null=True, blank=True, upload_to="competitions/", verbose_name="Imagem"
    )
    max_slots = models.PositiveIntegerField(
        default=0,
        verbose_name="Número de vagas",
        help_text="Se não quiser impor um limite de vagas, defina esse campo como 0",
    )

    class Meta:
        verbose_name = "Competição"
        verbose_name_plural = "Competições"

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("competitions:detail_competition", kwargs={"pk": self.pk})

    def can_edit(self, user):
        return user == self.organizer
