from django.db import models
from localflavor.br.models import BRStateField
from django.urls import reverse

from accounts.models import User
from sports.models import Modality


class Competition(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.PROTECT)
    modality = models.ForeignKey(Modality, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    description = models.TextField()
    datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=80)
    state = BRStateField()
    address = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to="competitions/")
    max_slots = models.PositiveIntegerField(help_text="Total de vagas disponíveis. Se não quiser impor um limite de vagas, defina esse campo como 0", default=0)

    class Meta:
        verbose_name = "Competição"
        verbose_name_plural = "Competições"

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("competitions:detail_competition", kwargs={"pk": self.pk})

    def can_edit(self, user):
        return user == self.organizer
