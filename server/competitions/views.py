from typing import Any
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Competition
from .forms import CompetitionForm


class CompetitionListView(ListView):
    model = Competition


class CompetitionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Competition
    form_class = CompetitionForm
    permission_required = "competitions.add_competition"

    def get_initial(self):
        return {"organizer": self.request.user}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Criar competição"
        return context


class CompetitionDetailView(DetailView):
    model = Competition


class CompetitionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Competition
    form_class = CompetitionForm
    permission_required = "competitions.change_competition"

    def has_permission(self) -> bool:
        authorized = super().has_permission()
        obj: Competition = self.get_object()
        return authorized and obj.can_edit(self.request.user)


# Create your views here.
class addTeamToCompetitionView(CreateView):
    model = Competition
    form_class = CompetitionForm
    template_name = "competitions/competition_sign.html"
    permission_required = "competitions.add_competition"

    # def has_permission(self) -> bool:
    #     has_permission = super().has_permission()
    #     team_leader = Competition.objects.get(pk=self.kwargs["competition"]).leader
    #     is_leader = self.request.user == team_leader
    #     return has_permission and is_leader

    # def get_initial(self):
    #     return {"competition": Competition.objects.get(pk=self.kwargs["competition"])}

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context["competition"] = Competition.objects.get(pk=self.kwargs["competition"])
    #     return context

    # def get_success_url(self) -> str:
    #     competition = Competition.objects.get(pk=self.kwargs["competition"])
    #     return reverse("competitions:detail_competition", kwargs={"pk": competition.id})