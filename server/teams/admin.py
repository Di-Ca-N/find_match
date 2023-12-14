from django.contrib import admin
from .models import Team, TeamMember


class TeamMemberInline(admin.StackedInline):
    model = TeamMember


class TeamAdmin(admin.ModelAdmin):
    model = Team
    inlines = [TeamMemberInline]
    list_display = ["__str__", "modality", "is_complete"]


admin.site.register(Team, TeamAdmin)
