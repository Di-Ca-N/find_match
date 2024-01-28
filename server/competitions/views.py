from typing import Any
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Competition, CompetitionSubscription
from .forms import CompetitionForm, CompetitionSubscribeForm


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
class addTeamToCompetitionView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = CompetitionSubscription
    form_class = CompetitionSubscribeForm
    template_name = "competitions/competition_subscribe.html"
    permission_required = "competitions.add_competitionsubscription"

    def has_permission(self) -> bool:
        has_permission = super().has_permission()
        team_leader = Competition.objects.get(pk=self.kwargs["competition"]).leader
        is_leader = self.request.user == team_leader
        return has_permission and is_leader

    def get_initial(self):
        competition_id = self.kwargs.get("pk")
        return {"competition": competition_id}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context["competition"] = Competition.objects.get(pk=self.kwargs["competition"])
        context["title"] = "Inscrever time"
        return context

    def get_success_url(self) -> str:
        competition = Competition.objects.get(pk=self.kwargs["pk"])
        return reverse("competitions:dashboard", kwargs={"pk": competition.pk})
    
    def form_valid(self, form):
        with transaction.atomic():
            competition = Competition.objects.select_for_update().get(pk=self.kwargs["pk"])
            response = super(addTeamToCompetitionView, self).form_valid(form)
            if competition.max_slots > 0:
                competition.max_slots -= 1
                competition.save()
                return response
            else:
                # error message
                self.request.session["error_message"] = "Não há mais vagas disponíveis"
                return HttpResponseRedirect(reverse("competitions:dashboard", kwargs={"pk": competition.pk}))

def CompetitionDashboardView(request, pk):
    return render(request, "competitions/dashboard.html", {"competition": Competition.objects.get(pk=pk)})