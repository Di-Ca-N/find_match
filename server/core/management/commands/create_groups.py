from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from competitions.models import Competition, CompetitionRate
from django.db.models import Q
from teams.models import Team, TeamMember


class Command(BaseCommand):
    help = "Create the required roles and permissions for the system"

    def handle(self, *args, **options):
        organizer_group, _ = Group.objects.get_or_create(name="organizers")
        competition_content_type = ContentType.objects.get_for_model(Competition)
        organizer_permissions = Permission.objects.filter(
            content_type=competition_content_type
        )
        organizer_group.permissions.set(organizer_permissions)
        print("Group 'organizers': OK")

        leader_group, _ = Group.objects.get_or_create(name="leaders")
        team_content_type = ContentType.objects.get_for_model(Team)
        team_member_content_type = ContentType.objects.get_for_model(TeamMember)
        competition_rate_content_type = ContentType.objects.get_for_model(CompetitionRate)
        leader_permissions = Permission.objects.filter(
            Q(content_type=team_member_content_type) | 
            Q(content_type=team_content_type) |
            Q(content_type=competition_rate_content_type)
        )
        leader_group.permissions.set(leader_permissions)
        print("Group 'leaders': OK")
