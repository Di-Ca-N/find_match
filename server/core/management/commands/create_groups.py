from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from competitions.models import Competition, CompetitionRate, CompetitionResults, CompetitionDocument, CompetitionSubscription
from django.db.models import Q
from teams.models import Team, TeamMember


class Command(BaseCommand):
    help = "Create the required roles and permissions for the system"

    def handle(self, *args, **options):
        organizer_group, _ = Group.objects.get_or_create(name="organizers")

        organizer_q = Q()
        for model in [Competition, CompetitionResults, CompetitionDocument]:
            content_type = ContentType.objects.get_for_model(model)
            organizer_q |= Q(content_type=content_type)
        organizer_group.permissions.set(Permission.objects.filter(organizer_q))
        print("Group 'organizers': OK")

        leader_group, _ = Group.objects.get_or_create(name="leaders")
        leader_q = Q()
        for model in [Team, TeamMember, CompetitionRate, CompetitionSubscription]:
            content_type = ContentType.objects.get_for_model(model)
            leader_q |= Q(content_type=content_type)
        leader_permissions = Permission.objects.filter(leader_q)
        leader_group.permissions.set(leader_permissions)
        print("Group 'leaders': OK")
