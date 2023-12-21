# Generated by Django 5.0 on 2023-12-17 02:35

import localflavor.br.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="cpf",
            field=localflavor.br.models.BRCPFField(
                max_length=14, null=True, unique=True, verbose_name="CPF"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=150, null=True, unique=True, verbose_name="username"
            ),
        ),
    ]