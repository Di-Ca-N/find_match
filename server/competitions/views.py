from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView

from .models import Competition
from .forms import CompetitionForm


class CompetitionListView(ListView):
    model = Competition


class CompetitionCreateView(CreateView):
    model = Competition
    form_class = CompetitionForm

    def get_initial(self):
        return {"organizer": self.request.user}


class CompetitionDetailView(DetailView):
    model = Competition


# Create your views here.
