from django.urls import path

from . import views

app_name = "competitions"
urlpatterns = [
    path("", views.CompetitionListView.as_view()),
    path("<int:pk>/", views.CompetitionDetailView.as_view(), name="detail_competition"),
    path(
        "update/<int:pk>/",
        views.CompetitionUpdateView.as_view(),
        name="update_competition",
    ),
    path("create/", views.CompetitionCreateView.as_view(), name="create_competition"),
]
