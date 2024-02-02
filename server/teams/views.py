from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.contrib import messages

from .forms import TeamForm, MemberForm
from .models import Team, TeamMember


class CreateTeamView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm

    def get_initial(self):
        return {"leader": self.request.user}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Cadastrar time"
        return context


class UpdateTeamView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm

    def get_initial(self) -> dict[str, Any]:
        return {"leader": self.request.user}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Alterar time"
        return context


class AddMemberToTeamView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TeamMember
    form_class = MemberForm
    template_name = "teams/team_member_form.html"
    permission_required = "teams.add_teammember"

    def has_permission(self) -> bool:
        has_permission = super().has_permission()
        team_leader = Team.objects.get(pk=self.kwargs["team"]).leader
        is_leader = self.request.user == team_leader
        return has_permission and is_leader

    def get_initial(self):
        return {"team": Team.objects.get(pk=self.kwargs["team"])}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["team"] = Team.objects.get(pk=self.kwargs["team"])
        return context

    def get_success_url(self) -> str:
        team = Team.objects.get(pk=self.kwargs["team"])
        return reverse("teams:detail_team", kwargs={"pk": team.id})


class ListTeams(LoginRequiredMixin, ListView):
    model = Team

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(leader=self.request.user)


class DetailTeam(DetailView):
    model = Team


class DeleteTeamMemberView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TeamMember
    
    def test_func(self):
        team = self.get_object().team
        return self.request.user == team.leader
    
    def form_valid(self, form):
        messages.success(self.request, f"Membro removido", "danger")
        return super().form_valid(form)
    

    def get_object(self, queryset = None) -> TeamMember:
        if queryset is None:
            queryset = self.get_queryset()
        
        return queryset.get(team=self.kwargs["team_id"], user=self.kwargs["user_id"])

    def get_success_url(self) -> str:
        return reverse("teams:detail_team", kwargs={"pk": self.kwargs["team_id"]})
