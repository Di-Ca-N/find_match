# Generated by Django 5.0 on 2024-02-02 01:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("competitions", "0010_rename_avaliacoes_competition_raters_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="competitionrate",
            options={
                "verbose_name": "Avaliação de Competição",
                "verbose_name_plural": "Avaliações de Competições",
            },
        ),
    ]