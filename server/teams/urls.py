from django.urls import path

from . import views

app_name = "teams"
urlpatterns = [
    path("create/", views.CreateTeamView.as_view(), name="create_team"),
    path("<int:team>/add_member/", views.AddMemberToTeamView.as_view()),
    path("<int:pk>/", views.DetailTeam.as_view(), name="detail_team"),
    path("", views.ListTeams.as_view()),
]
