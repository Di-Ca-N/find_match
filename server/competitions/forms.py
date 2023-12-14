from django import forms
from accounts.models import User
from .models import Competition


class CompetitionForm(forms.ModelForm):
    organizer = forms.ModelChoiceField(
        User.objects.all(), disabled=True, widget=forms.widgets.HiddenInput()
    )

    class Meta:
        model = Competition
        fields = "__all__"
        widgets = {
            "datetime": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"})
        }
