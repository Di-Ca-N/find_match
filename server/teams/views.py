from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import TeamForm, MemberForm
from .models import Team, TeamMember


class CreateTeamView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm

    def get_initial(self):
        return {"leader": self.request.user}


class AddMemberToTeamView(LoginRequiredMixin, CreateView):
    model = TeamMember
    form_class = MemberForm
    template_name = "teams/team_member_form.html"

    def get_initial(self):
        return {"team": Team.objects.get(pk=self.kwargs["team"])}


class ListTeams(LoginRequiredMixin, ListView):
    model = Team

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(leader=self.request.user)


class DetailTeam(DetailView):
    model = Team
