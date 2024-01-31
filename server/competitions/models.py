from django.db import models
from localflavor.br.models import BRStateField
from django.urls import reverse
from django.utils import timezone

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
    datetime_end = models.DateTimeField(verbose_name="Data e Horário de término")
    subscription_until = models.DateTimeField(verbose_name="Prazo de inscrição")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    city = models.CharField(max_length=80, verbose_name="Cidade", blank=True)
    state = BRStateField(verbose_name="Estado", blank=True)
    address = models.CharField(max_length=100, verbose_name="Endereço", blank=True)
    image = models.ImageField(
        null=True, blank=True, upload_to="competitions/", verbose_name="Imagem"
    )
    max_slots = models.PositiveIntegerField(
        default=0,
        verbose_name="Número de vagas",
        help_text="Se não quiser impor um limite de vagas, defina esse campo como 0",
    )
    subscription_price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Preço da inscrição", default=0
    )
    raters = models.ManyToManyField(User, through="CompetitionRate", related_name="+")

    class Meta:
        verbose_name = "Competição"
        verbose_name_plural = "Competições"

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("competitions:detail_competition", kwargs={"pk": self.pk})

    def can_edit(self, user):
        return user == self.organizer

    def competition_ended(self):
        return self.datetime_end < timezone.now()

    def can_evaluate_competition(self, user):
        user_already_evaluated = self.raters.filter(pk=user.id).exists()

        # ToDo: Adicionar restrição de usuário estar cadastrado na competição
        return not user_already_evaluated and self.competition_ended()


class RatingChoices(models.IntegerChoices):
    EXCELLENT = (5, "Excelente")
    VERY_GOOD = (4, "Ótimo")
    GOOD = (3, "Bom")
    FAIR = (2, "Regular")
    POOR = (1, "Ruim")


class CompetitionRate(models.Model):
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    rating = models.PositiveIntegerField(choices=RatingChoices)
    observations = models.TextField()

    class Meta:
        verbose_name = "Avaliação de Competição"
        verbose_name_plural = "Avaliações de Competições"

    def __str__(self):
        return f"Avaliação de {self.competition} por {self.user}"
