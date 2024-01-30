from django.urls import path, include
from django.contrib.auth import urls as auth_urls
from .views import CreateUserView
from .views import organizer_request_view

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="register"),
    path("", include(auth_urls)),
    path('organizer-request/', organizer_request_view, name='organizer_request'),
]


app_name = "accounts"
