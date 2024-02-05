from django.urls import path

from . import views

app_name = "competitions"
urlpatterns = [
    path(
        "<int:pk>/subscribe/",
        views.AddTeamToCompetitionView.as_view(),
        name="competition_subscribe",
    ),
    path("", views.CompetitionListView.as_view(), name="list_competition"),
    path("<int:pk>/", views.CompetitionDetailView.as_view(), name="detail_competition"),
    path(
        "update/<int:pk>/",
        views.CompetitionUpdateView.as_view(),
        name="update_competition",
    ),
    path("create/", views.CompetitionCreateView.as_view(), name="create_competition"),
    path("dashboard/<int:pk>", views.CompetitionDashboardView, name="dashboard"),
    path(
        "<int:competition_id>/rate/",
        views.RateCompetitionView.as_view(),
        name="rate_competition",
    ),
    path("my/", views.MyCompetitionsView.as_view(), name="my_competitions"),
    path("my/<int:pk>", views.cancelSubscriptionView.as_view(), name="remove_subscription"),
    path('<int:pk>/assign-winners/', views.CompetitionWinnersView.as_view(), name='assign_winners'),
    path("<int:competition_id>/documents/add", views.AddCompetitionDocument.as_view(), name="add_document"),
    path("<int:pk>/manage", views.ManageCompetitionView.as_view(), name="manage_competition"),
    path("<int:competition_id>/documents/<int:document_id>/delete", views.RemoveCompetitionDocument.as_view(), name="delete_document")
]
