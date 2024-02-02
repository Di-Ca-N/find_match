from django import forms
from accounts.models import User
from .models import Competition, CompetitionSubscription, Team


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
            "subscription_until": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"})
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
        self.user = kwargs.pop("user",None)
        super(CompetitionSubscribeForm, self).__init__(*args, **kwargs)
        if self.user is not None:
            self.fields["team"].queryset = Team.objects.filter(leader=self.user)
       
