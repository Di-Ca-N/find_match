from typing import Any
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy

from .models import Competition, CompetitionRate
from .forms import CompetitionForm, CompetitionRateForm


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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[
            "user_can_evaluate_competition"
        ] = self.get_object().can_evaluate_competition(self.request.user)
        return context


class CompetitionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Competition
    form_class = CompetitionForm
    permission_required = "competitions.change_competition"

    def has_permission(self) -> bool:
        authorized = super().has_permission()
        obj: Competition = self.get_object()
        return authorized and obj.can_edit(self.request.user)


class RateCompetitionView(UserPassesTestMixin, CreateView):
    model = CompetitionRate
    template_name = "competitions/rate_competition.html"
    form_class = CompetitionRateForm
    success_url = reverse_lazy("home")

    def test_func(self):
        competition = Competition.objects.get(pk=self.kwargs["competition_id"])
        return competition.can_evaluate_competition(self.request.user)

    def get_initial(self) -> dict[str, Any]:
        return {
            "user": self.request.user,
            "competition": Competition.objects.get(pk=self.kwargs["competition_id"]),
        }

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["competition"] = Competition.objects.get(
            pk=self.kwargs["competition_id"]
        )
        return context


class MyCompetitionsView(LoginRequiredMixin, TemplateView):
    template_name = "competitions/my_competitions.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        organized_competitions = Competition.objects.filter(organizer=self.request.user)
        
        context["organized_competitions"] = organized_competitions
        return context
