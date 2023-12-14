from django import forms
from localflavor.br.forms import BRCPFField
from .models import Team, TeamMember
from accounts.models import User


class TeamForm(forms.ModelForm):
    leader = forms.ModelChoiceField(queryset=User.objects.all(), disabled=True, widget=forms.widgets.HiddenInput())

    class Meta:
        model = Team
        fields = ['name', 'leader', 'modality']

class MemberForm(forms.ModelForm):
    cpf = BRCPFField()
    name = forms.CharField()
    team = forms.ModelChoiceField(queryset=Team.objects.all(), disabled=True, widget=forms.widgets.HiddenInput())    

    class Meta:
        model = TeamMember
        fields = ['team']

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get("cpf")
        team = cleaned_data.get("team")
        
        if TeamMember.objects.filter(player__account__cpf=cpf, team=team).exists():
            self.add_error("cpf", "Jogador informado já está no time")

    def save(self, commit=True):
        user, _ = User.objects.get_or_create(
            cpf=self.cleaned_data["cpf"],
            defaults={"first_name":self.cleaned_data["name"]}
        )
        self.instance.user = user
        return super().save(commit)

