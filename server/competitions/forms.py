from django import forms
from accounts.models import User
from .models import Competition


class CompetitionForm(forms.ModelForm):
    organizer = forms.ModelChoiceField(
        User.objects.all(), disabled=True, widget=forms.widgets.HiddenInput()
    )

    class Meta:
        model = Competition
        fields = ["title", "modality", "description", "datetime", "city", "state", "address", "image", "max_slots", "subscription_price", "organizer"]
        widgets = {
            "datetime": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"})
        }
