from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=30)


class Modality(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    team_size = models.PositiveSmallIntegerField()
