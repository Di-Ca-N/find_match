from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Esporte"
        verbose_name_plural = "Esportes"

    def __str__(self):
        return f"{self.name}"


class Modality(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    team_size = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Modalidade"
        verbose_name_plural = "Modalidades"

    def __str__(self):
        return f"{self.sport} - {self.name}"
