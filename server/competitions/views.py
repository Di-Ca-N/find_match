from typing import Any
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    TemplateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponseRedirect
from django.db import transaction
from django.urls import reverse_lazy
from .models import Competition, CompetitionSubscription, CompetitionRate, SubscriptionStatus, CompetitionResults, Team
from .forms import CompetitionForm, CompetitionSubscribeForm, CompetitionRateForm, CompetitionWinnersForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages


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
    fields = []

    def has_permission(self) -> bool:
        authorized = super().has_permission()
        obj: Competition = self.get_object()
        return authorized and obj.can_edit(self.request.user)


# Create your views here.
class addTeamToCompetitionView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, CreateView):
    model = CompetitionSubscription
    form_class = CompetitionSubscribeForm
    template_name = "competitions/competition_subscribe.html"
    permission_required = "competitions.add_competitionsubscription"

    # def has_permission(self) -> bool:
    #     has_permission = super().has_permission()
    #     return has_permission

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
        team = form.instance.team

        if team.leader != self.request.user:
            self.request.session["error_message"] = "Você não é o líder do time"
            raise PermissionDenied("Você não tem permissão para inscrever este time.")
        try:
            competition = Competition.objects.get(pk=self.kwargs["pk"])
            slots = competition.competitionsubscription_set.filter(status=SubscriptionStatus.CONFIRMED).count()

            if competition.max_slots - slots > 0:
                response = super().form_valid(form)
                return response
            else:
                # error message
                messages.error(self.request, "Competição sem vagas disponíveis", "danger")
                return HttpResponseRedirect(
                    reverse("competitions:dashboard", kwargs={"pk": competition.pk})
                )
        except ValidationError as e:
            # Se uma ValidationError for capturada, adiciona os erros ao formulário
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["modality"] = Competition.objects.get(pk=self.kwargs["pk"]).modality
        return kwargs

class cancelSubscriptionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CompetitionSubscription

    def test_func(self):
        subscription = self.get_object()
        return subscription.team.leader == self.request.user

    def get_success_url(self) -> str:
        competition = self.get_object().competition
        return reverse("competitions:my_competitions", kwargs={"pk": competition.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Cancelar inscrição"
        return context

    def post(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.cancel()
        return HttpResponseRedirect(self.get_success_url())

class CompetitionWinnersView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Competition
    form_class = CompetitionWinnersForm
    permission_required = "competitions.change_competition"
    success_url = reverse_lazy('my_competitions')
    template_name = "competitions/assign_winners.html"

    def form_valid(self, form):
        competition = get_object_or_404(Competition, pk=self.kwargs['pk'])
        if not self.request.user == competition.organizer:
            form.add_error(None, "Você não tem permissão para atribuir vencedores a esta competição.")
            return self.form_invalid(form)
        
        placements = {
            'first_place': 1,
            'second_place': 2,
            'third_place': 3,
        }

        for field_name, placement in placements.items():
            team_id = form.cleaned_data.get(field_name)
            if team_id:
                team = get_object_or_404(Team, pk=team_id)
                CompetitionResults.objects.update_or_create(
                    competition=competition,
                    placement=placement,
                    defaults={'team': team}
                )

        return super().form_valid(form)

    def test_func(self):
        competition = self.get_object()
        return self.request.user == competition.organizer
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['competition_id'] = self.kwargs['pk']
        return kwargs


def CompetitionDashboardView(request, pk):
    return render(
        request,
        "competitions/dashboard.html",
        {"competition": Competition.objects.get(pk=pk)},
    )


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
        subscribed_events = Competition.objects.filter(subscribed_teams__leader=self.request.user).distinct()
        my_subscriptions = CompetitionSubscription.objects.filter(team__leader=self.request.user)

        context["organized_competitions"] = organized_competitions
        context["subscribed_events"] = subscribed_events
        context["my_subscriptions"] = my_subscriptions
        return context
