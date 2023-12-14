from django.views.generic import CreateView
from .forms import TeamForm, MemberForm
from .models import Team, TeamMember


class CreateTeamView(CreateView):
    model = Team
    form_class = TeamForm

    def get_initial(self):
        return {
            "leader": self.request.user
        }


class AddMemberToTeamView(CreateView):
    model = TeamMember
    form_class = MemberForm
    template_name = 'teams/team_member_form.html'
    
    def get_initial(self):
        return {
            "team": Team.objects.get(pk=self.kwargs["team"])
        }
