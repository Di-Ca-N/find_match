from django.db import models
from accounts.models import User
from sports.models import Modality


class Team(models.Model):
    name = models.CharField(max_length=50)
    leader = models.ForeignKey(User, on_delete=models.PROTECT, related_name="leads")
    members = models.ManyToManyField(User, through="teams.TeamMember")
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_team_name')
        ]

    def __str__(self):
        return f"{self.name}"
    
    def get_num_members(self):
        return self.members.count() + 1

    def is_complete(self):
        return self.get_num_members() == self.modality.team_size        

class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
