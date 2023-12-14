from django.db import models
from accounts.models import User
from sports.models import Modality


class Player(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"


class Team(models.Model):
    name = models.CharField(max_length=50)
    leader = models.ForeignKey(Player, on_delete=models.PROTECT, related_name="leads")
    members = models.ManyToManyField(Player, through="teams.TeamMember")
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_team_name')
        ]

    def __str__(self):
        return f"{self.name}"


class TeamMember(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


# Create your models here.