from django import forms
from accounts.models import User
from .models import Competition, CompetitionRate


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
            "datetime": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"}),
            "subscription_until": forms.widgets.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }


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
