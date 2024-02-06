from django.db import models
from django.urls import reverse

from accounts.models import User
from sports.models import Modality


class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nome")
    leader = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="leads", verbose_name="Líder"
    )
    members = models.ManyToManyField(
        User, through="teams.TeamMember", verbose_name="Membros"
    )
    modality = models.ForeignKey(
        Modality, on_delete=models.CASCADE, verbose_name="Modalidade"
    )

    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_team_name")
        ]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("teams:detail_team", kwargs={"pk": self.pk})

    def get_members(self):
        members = [self.leader]
        members.extend(self.members.all())
        return members

    def get_num_members(self):
        return self.members.count() + 1

    def is_complete(self):
        return self.get_num_members() == self.modality.team_size
    
    def get_subscriptions(self):
        return self.subscriptions.all()
    
    def get_results(self):
        return self.team_results.all()

    def is_busy_at(self, start, end):
        return self.subscriptions.non_canceled().happening_between(start, end).exists()


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
