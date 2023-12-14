from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse

from .models import User
from .forms import UserCreationForm


class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "registration/register.html"

    def get_success_url(self) -> str:
        return reverse("home")
    
