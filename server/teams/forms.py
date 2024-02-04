from django import forms
from localflavor.br.forms import BRCPFField
from .models import Team, TeamMember
from accounts.models import User


class TeamForm(forms.ModelForm):
    leader = forms.ModelChoiceField(
        queryset=User.objects.all(), disabled=True, widget=forms.widgets.HiddenInput()
    )

    class Meta:
        model = Team
        fields = ["name", "leader", "modality"]


class MemberForm(forms.ModelForm):
    cpf = BRCPFField()
    first_name = forms.CharField(max_length=150, label="Nome")
    last_name = forms.CharField(max_length=150, label="Sobrenome")
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(), disabled=True, widget=forms.widgets.HiddenInput()
    )

    class Meta:
        model = TeamMember
        fields = ["team"]

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get("cpf")
        team: Team = cleaned_data.get("team")

        if team.members.filter(cpf=cpf).exists() or team.leader.cpf == cpf:
            self.add_error("cpf", "Jogador informado já está no time")

    def save(self, commit=True):
        user, _ = User.objects.get_or_create(
            cpf=self.cleaned_data["cpf"],
            defaults={
                "first_name": self.cleaned_data["first_name"],
                "last_name": self.cleaned_data["last_name"],
            },
        )
        self.instance.user = user
        return super().save(commit)
