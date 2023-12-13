from django.urls import path

from . import views

app_name = "competitions"
urlpatterns = [
    path("", views.CompetitionListView.as_view()),
    path("<int:pk>/", views.CompetitionDetailView.as_view(), name="detail"),
    path("create/", views.CompetitionCreateView.as_view()),
]
