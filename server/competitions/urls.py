from django.urls import path

from . import views

app_name = "competitions"
urlpatterns = [
    path("<int:pk>/subscribe/", views.addTeamToCompetitionView.as_view(), name="competition_subscribe"),
    path("", views.CompetitionListView.as_view(), name="list_competition"),
    path("<int:pk>/", views.CompetitionDetailView.as_view(), name="detail_competition"),
    path("update/<int:pk>/", views.CompetitionUpdateView.as_view(), name="update_competition"),
    path("create/", views.CompetitionCreateView.as_view(), name="create_competition"),
    path("dashboard/<int:pk>", views.CompetitionDashboardView, name="dashboard"),
]
