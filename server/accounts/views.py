from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .models import User
from .forms import UserCreationForm
from .forms import OrganizerRequestForm


class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "registration/register.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        try:
            leaders_group = Group.objects.get(name="leaders")
            user.groups.add(leaders_group)
            user.save()
        except Group.DoesNotExist:
            pass
        return response

    def get_success_url(self) -> str:
        return reverse("home")

def organizer_request_view(request):
    if request.method == 'POST':
        form = OrganizerRequestForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email to administrators)
            reason = form.cleaned_data['reason']
            
            return redirect('home')
    else:
        form = OrganizerRequestForm()

    return render(request, 'organizer_requests/organizer_request_form.html', {'form': form})