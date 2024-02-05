from typing import Any
from django.views.generic import TemplateView

from competitions.models import Competition


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["competitions"] = Competition.objects.order_by("?")[:3]
        return context


# Create your views here.
