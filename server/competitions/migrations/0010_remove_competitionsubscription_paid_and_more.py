# Generated by Django 5.0 on 2024-01-27 22:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("competitions", "0009_competitionsubscription"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="competitionsubscription",
            name="paid",
        ),
        migrations.AddField(
            model_name="competitionsubscription",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pendente"),
                    ("CONFIRMED", "Confirmada"),
                    ("CANCELED", "Cancelada"),
                ],
                default="PENDING",
                max_length=10,
            ),
        ),
    ]