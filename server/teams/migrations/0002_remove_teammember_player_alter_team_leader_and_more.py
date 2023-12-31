# Generated by Django 5.0 on 2023-12-14 21:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teams", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teammember",
            name="player",
        ),
        migrations.AlterField(
            model_name="team",
            name="leader",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="leads",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="teammember",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="team",
            name="members",
            field=models.ManyToManyField(
                through="teams.TeamMember", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="Player",
        ),
    ]
