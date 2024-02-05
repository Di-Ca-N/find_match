# Generated by Django 5.0 on 2024-02-04 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("competitions", "0014_competitionresults"),
    ]

    operations = [
        migrations.AlterField(
            model_name="competitionresults",
            name="competition",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="results",
                to="competitions.competition",
            ),
        ),
    ]
