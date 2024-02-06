from typing import Any
from django.db.models.base import Model as Model
from django.urls.exceptions import NoReverseMatch
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    TemplateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy
from .models import (
    Competition,
    CompetitionSubscription,
    CompetitionRate,
    CompetitionResults,
    CompetitionDocument,
    SubscriptionStatus,
    OrganizerRequest,
)
from .forms import (
    CompetitionForm,
    CompetitionSubscribeForm,
    CompetitionRateForm,
    CompetitionWinnersForm,
    CompetitionDocumentForm,
    OrganizerRequestForm,
)
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
        winners = self.get_object().results.all().order_by("place")
        team_winners = []
        class_names = ['podium-first-member', 'podium-second-member', 'podium-third-member']
        for i in range(3):
            try:
                winner = winners[i]
            except IndexError:
                winner = None
            team_winners.append({'winner': winner, 'class': class_names[i]})

        context = super().get_context_data(**kwargs)
        context[
            "user_can_evaluate_competition"
        ] = self.get_object().can_evaluate_competition(self.request.user)
        context["team_winners"] =  team_winners
        return context


class AddTeamToCompetitionView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CompetitionSubscription
    form_class = CompetitionSubscribeForm
    template_name = "competitions/competition_subscribe.html"
    permission_required = "competitions.add_competitionsubscription"

    def get_initial(self):
        competition_id = self.kwargs.get("pk")
        return {"competition": competition_id}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["competition"] = Competition.objects.get(pk=self.kwargs["pk"])
        context["title"] = "Inscrever time"
        return context

    def get_success_url(self) -> str:
        return reverse("competitions:my_competitions")

    def form_valid(self, form):
        team = form.instance.team

        if team.leader != self.request.user:
            self.request.session["error_message"] = "Você não é o líder do time"
            raise PermissionDenied("Você não tem permissão para inscrever este time.")

        try:
            response = super().form_valid(form)
            messages.success(self.request, "O time foi cadastrado na competição")
            return response
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


class CancelSubscriptionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CompetitionSubscription
    fields = []
    template_name = "competitions/confirm_cancel_subscription.html"
    success_url = reverse_lazy("competitions:my_competitions")

    def test_func(self):
        subscription = self.get_object()
        return subscription.team.leader == self.request.user

    def form_valid(self, form):
        subscription = form.instance
        subscription.cancel()
        messages.success(self.request, "A inscrição foi cancelada")
        return super().form_valid(form)


class CompetitionWinnersView(
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Competition
    form_class = CompetitionWinnersForm
    permission_required = "competitions.change_competition"
    success_url = reverse_lazy("competitions:my_competitions")
    template_name = "competitions/assign_winners.html"

    def form_valid(self, form):
        competition = get_object_or_404(Competition, pk=self.kwargs["pk"])
        if not self.request.user == competition.organizer:
            form.add_error(
                None,
                "Você não tem permissão para atribuir vencedores a esta competição.",
            )
            return self.form_invalid(form)

        placements = {
            "first_place": 1,
            "second_place": 2,
            "third_place": 3,
        }

        # cleaned_data is a dictionary with the form fields and their values, after is_valid() is called
        # it contains only the fields that have been validated

        for field_name, placement in placements.items():
            team = form.cleaned_data.get(field_name) # get the team from the form cleaned data
            if team is not None:
                CompetitionResults.objects.update_or_create(
                    competition=competition, place=placement, defaults={"team": team}
                )

        return super().form_valid(form)

    def test_func(self):
        competition = self.get_object()
        return self.request.user == competition.organizer

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["competition_id"] = self.kwargs["pk"]
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
        subscribed_events = Competition.objects.filter(
            subscribed_teams__leader=self.request.user
        ).distinct()

        context["organized_competitions"] = organized_competitions
        context["subscribed_events"] = subscribed_events
        context["confirmed_subscriptions"] = CompetitionSubscription.objects.filter(
            team__leader=self.request.user, status=SubscriptionStatus.CONFIRMED
        )
        context["pending_subscriptions"] = CompetitionSubscription.objects.filter(
            team__leader=self.request.user, status=SubscriptionStatus.PENDING
        )
        context["show_become_organizer_button"] = OrganizerRequest.can_request_account(
            self.request.user
        )
        return context


class CompetitionManagementBaseView(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        competition = Competition.objects.get(pk=self.get_object_pk())
        return self.request.user == competition.organizer

    def get_object_pk(self):
        return self.kwargs.get("pk") or self.kwargs.get("competition_id")

    def get_success_url(self) -> str:
        try:
            return reverse(
                "competitions:manage_competition",
                kwargs={"competition_id": self.get_object_pk()},
            )
        except NoReverseMatch:
            return reverse(
                "competitions:manage_competition", kwargs={"pk": self.get_object_pk()}
            )


class RemoveCompetitionDocument(CompetitionManagementBaseView, DeleteView):
    model = CompetitionDocument

    def get_object(self) -> Model:
        return CompetitionDocument.objects.get(pk=self.kwargs["document_id"])


class AddCompetitionDocument(CompetitionManagementBaseView, CreateView):
    model = CompetitionDocument
    form_class = CompetitionDocumentForm
    template_name = "competitions/add_documents.html"

    def get_initial(self) -> dict[str, Any]:
        competition = Competition.objects.get(pk=self.kwargs["competition_id"])
        return {"competition": competition}


class ManageCompetitionView(CompetitionManagementBaseView, DetailView):
    model = Competition
    template_name = "competitions/manage_competition.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["confirmed_subscriptions"] = self.get_object().subscriptions.confirmed()
        context["pending_subscriptions"] = self.get_object().subscriptions.pending()
        return context


class CompetitionUpdateView(CompetitionManagementBaseView, UpdateView):
    model = Competition
    form_class = CompetitionForm
    permission_required = "competitions.change_competition"

    def has_permission(self) -> bool:
        authorized = super().has_permission()
        obj: Competition = self.get_object()
        return authorized and obj.can_edit(self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Atualizar Competição"
        return context


class PaySubscriptionView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = CompetitionSubscription
    fields = []
    template_name = "competitions/pay_subscription.html"
    success_url = reverse_lazy("competitions:my_competitions")

    def test_func(self):
        return self.request.user == self.get_object().team.leader

    def form_valid(self, form):
        instance: CompetitionSubscription = form.instance
        if not instance.is_pending():
            form.add_error(None, "Só é possível confirmar inscrições pendentes")
            return self.form_invalid(form)
        instance.confirm()
        return super().form_valid(form)


class RequestOrganizerAccountView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = OrganizerRequest
    form_class = OrganizerRequestForm
    template_name = "competitions/request_organizer_account.html"
    success_url = reverse_lazy("competitions:my_competitions")

    def test_func(self):
        return OrganizerRequest.can_request_account(self.request.user)

    def get_initial(self) -> dict[str, Any]:
        return {"user": self.request.user}

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Sua solicitação foi enviada e está sob revisão")
        return response

class CompetitionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Competition
    success_url = reverse_lazy("competitions:my_competitions")

    def test_func(self):
        competition = self.get_object()
        return self.request.user == competition.organizer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(organizer=self.request.user)