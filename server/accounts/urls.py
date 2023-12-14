from django.urls import path, include
from django.contrib.auth import urls as auth_urls
from .views import CreateUserView

urlpatterns = [
    path("create/", CreateUserView.as_view()),
    path("", include(auth_urls))
]


app_name = "accounts"
