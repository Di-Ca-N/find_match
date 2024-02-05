from django import forms
from accounts.models import User
from .models import (
    Competition,
    CompetitionDocument,
    CompetitionResults,
    CompetitionSubscription,
    Team,
    CompetitionRate,
    OrganizerRequest,
)


class CompetitionForm(forms.ModelForm):
    organizer = forms.ModelChoiceField(
        User.objects.all(), disabled=True, widget=forms.widgets.HiddenInput()
    )

    class Meta:
        model = Competition
        fields = [
            "title",
            "modality",
            "description",
            "datetime",
            "datetime_end",
            "city",
            "state",
            "address",
            "image",
            "max_slots",
            "subscription_price",
            "subscription_until",
            "organizer",
        ]
        widgets = {
            "datetime": forms.widgets.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "datetime_end": forms.widgets.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "subscription_until": forms.widgets.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }


class CompetitionSubscribeForm(forms.ModelForm):
    competition = forms.ModelChoiceField(
        Competition.objects.all(), disabled=True, widget=forms.widgets.HiddenInput()
    )

    class Meta:
        model = CompetitionSubscription
        fields = [
            "team",
            "competition",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        modality = kwargs.pop("modality", None)
        super(CompetitionSubscribeForm, self).__init__(*args, **kwargs)

        if self.user is not None:
            self.fields["team"].queryset = Team.objects.filter(
                leader=self.user, modality=modality
            )

    def clean(self):
        competition: Competition = self.cleaned_data["competition"]
        team = self.cleaned_data["team"]
        competition.check_team_subscription(team)


class CompetitionRateForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        User.objects.all(), disabled=True, widget=forms.widgets.HiddenInput()
    )
    competition = forms.ModelChoiceField(
        Competition.objects.all(), disabled=True, widget=forms.widgets.HiddenInput()
    )

    class Meta:
        model = CompetitionRate
        fields = ["competition", "user", "rating", "observations"]


class CompetitionWinnersForm(forms.ModelForm):
    first_place = forms.ModelChoiceField(
        queryset=Team.objects.none(), label="1st Place"
    )
    second_place = forms.ModelChoiceField(
        queryset=Team.objects.none(), label="2nd Place"
    )
    third_place = forms.ModelChoiceField(
        queryset=Team.objects.none(), label="3rd Place"
    )

    class Meta:
        model = CompetitionResults
        fields = []

    def __init__(self, *args, **kwargs):
        competition_id = kwargs.pop("competition_id", None)
        super(CompetitionWinnersForm, self).__init__(*args, **kwargs)
        self.fields["first_place"].queryset = Team.objects.filter(
            competitions__id=competition_id
        )
        self.fields["second_place"].queryset = Team.objects.filter(
            competitions__id=competition_id
        )
        self.fields["third_place"].queryset = Team.objects.filter(
            competitions__id=competition_id
        )


class CompetitionDocumentForm(forms.ModelForm):
    competition = forms.ModelChoiceField(
        Competition.objects.all(), disabled=True, widget=forms.widgets.HiddenInput()
    )

    class Meta:
        model = CompetitionDocument
        fields = ["competition", "name", "file"]


class OrganizerRequestForm(forms.ModelForm):
    class Meta:
        model = OrganizerRequest
        fields = [
            "user",
            "request_reason",
        ]
        widgets = {"user": forms.widgets.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].disabled = True
