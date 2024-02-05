from django.db import models
from django.forms import ValidationError
from localflavor.br.models import BRStateField
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group

from accounts.models import User
from sports.models import Modality
from teams.models import Team

from django.db.models import Q


class CompetitionManager(models.Manager):
    def finalized(self):
        return self.filter(datetime_end__lt=timezone.now())

    def active(self):
        return self.filter(datetime__lt=timezone.now(), datetime_end__gt=timezone.now())

    def upcoming(self):
        return self.filter(datetime__gt=timezone.now())


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
    subscribed_teams = models.ManyToManyField(
        Team,
        through="competitions.CompetitionSubscription",
        related_name="competitions",
    )

    raters = models.ManyToManyField(User, through="CompetitionRate", related_name="+")

    objects = CompetitionManager()

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

    def confirmed_subscriptions(self):
        return self.subscriptions.filter(status=SubscriptionStatus.CONFIRMED)

    def has_open_slots(self):
        return (
            self.max_slots == 0
            or self.subscriptions.confirmed().count() < self.max_slots
        )

    def check_team_subscription(self, team):
        if not self.has_open_slots():
            raise ValidationError("Competição não tem vagas")

        team_already_subscribed = (
            self.subscriptions.non_canceled().filter(team=team).exists()
        )
        if team_already_subscribed:
            raise ValidationError("Este time já está inscrito nesta competição.")

        if team.is_busy_at(self.datetime, self.datetime_end):
            raise ValidationError(
                "Este time já está inscrito em outra competição no mesmo horário."
            )

        if not team.is_complete():
            raise ValidationError("Time não está completo")

        if team.modality != self.modality:
            raise ValidationError("Time não é da modalidade correta")

        for member in team.get_members():
            if CompetitionSubscription.objects.filter(
                ~Q(team=team),
                Q(team__members=member) | Q(team__leader=member),
                competition=self,
            ).exists():
                raise ValidationError(
                    f"O membro {member.get_full_name()} já está inscrito em outra competição no mesmo horário."
                )


class SubscriptionStatus(models.TextChoices):
    PENDING = "PENDING", "Pendente"
    CONFIRMED = "CONFIRMED", "Confirmada"
    CANCELED = "CANCELED", "Cancelada"


class SubscriptionQuerySet(models.QuerySet):
    def confirmed(self):
        return self.filter(status=SubscriptionStatus.CONFIRMED)

    def non_canceled(self):
        return self.exclude(status=SubscriptionStatus.CANCELED)

    def pending(self):
        return self.filter(status=SubscriptionStatus.PENDING)

    def canceled(self):
        return self.filter(status=SubscriptionStatus.CANCELED)

    def happening_between(self, start, end):
        return self.filter(
            competition__datetime__lt=end, competition__datetime_end__gt=start
        )


class CompetitionSubscription(models.Model):
    competition = models.ForeignKey(
        Competition, on_delete=models.PROTECT, verbose_name="Competição", related_name="subscriptions"
    )
    team = models.ForeignKey(Team, on_delete=models.PROTECT, verbose_name="Time", related_name="subscriptions")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    status = models.CharField(
        max_length=10,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.PENDING,
    )
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Pago em")

    objects = SubscriptionQuerySet.as_manager()

    def is_confirmed(self):
        return self.status == SubscriptionStatus.CONFIRMED

    def is_canceled(self):
        return self.status == SubscriptionStatus.CANCELED

    def is_pending(self):
        return self.status == SubscriptionStatus.PENDING

    def confirm(self):
        self.paid_at = timezone.now()
        self.status = SubscriptionStatus.CONFIRMED
        self.save()

    def cancel(self):
        self.status = SubscriptionStatus.CANCELED
        self.save()

    def save(self, *args, **kwargs):
        if self.competition.subscription_price == 0:
            self.status = SubscriptionStatus.CONFIRMED
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"

    def __str__(self):
        return f"Inscrição de {self.team} em {self.competition}"


class CompetitionResults(models.Model):
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name="results"
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team_results"
    )
    place = models.PositiveIntegerField(verbose_name="Colocação")

    class Meta:
        verbose_name = "Resultado de Competição"
        verbose_name_plural = "Resultados de Competições"

    def __str__(self):
        return f"{self.team.name}"


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


class CompetitionDocument(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Competição",
    )
    name = models.CharField(max_length=50, verbose_name="Nome do arquivo")
    file = models.FileField(verbose_name="Arquivo")
    creation = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Documento de Competição"
        verbose_name_plural = "Documentos de Competições"
        constraints = [
            models.UniqueConstraint(
                fields=["competition", "name"],
                name="unique_document_name_per_competition",
            )
        ]


class OrganizerRequestStatus(models.TextChoices):
    PENDING = "PENDING", "Pendente"
    APPROVED = "APPROVED", "Aprovada"
    REJECTED = "REJECTED", "Rejeitada"


class OrganizerRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organizer_requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    request_reason = models.TextField(verbose_name="Motivo da Solicitação")
    status = models.CharField(
        max_length=10,
        choices=OrganizerRequestStatus.choices,
        default=OrganizerRequestStatus.PENDING,
    )

    class Meta:
        verbose_name = "Requisição de Conta de Organizador"
        verbose_name_plural = "Requisições de Conta de Organizador"

    def __str__(self):
        return f"Requisição de {self.user.get_full_name()}"

    def approve(self):
        self.status = OrganizerRequestStatus.APPROVED
        self.user.groups.add(Group.objects.get(name="organizers"))
        self.save()

    def reject(self):
        self.status = OrganizerRequestStatus.REJECTED
        self.save()

    @staticmethod
    def can_request_account(user: User):
        account_age = timezone.now() - user.date_joined
        num_competitions = (
            CompetitionSubscription.objects.confirmed()
            .filter(team__leader=user)
            .count()
        )
        return account_age.days > 30 and num_competitions >= 5
