from django.urls import path

from . import views

app_name = 'teams'
urlpatterns = [
    path("create/", views.CreateTeamView.as_view()),
    path("<int:team>/add_member/", views.AddMemberToTeamView.as_view()),
]
