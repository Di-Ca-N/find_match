from django.contrib import admin
from .models import Team, Player, TeamMember


class TeamMemberInline(admin.StackedInline):
    model = TeamMember


class TeamAdmin(admin.ModelAdmin):
    model = Team
    inlines = [TeamMemberInline]


admin.site.register(Player)
admin.site.register(Team, TeamAdmin)
