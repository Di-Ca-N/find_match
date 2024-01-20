from django.utils import render, timezone
from django.views.generic import ListView
from .models import Competition


def list_competitions(request):
	# Lógica
	competitions = Competition.objects.all() # SELECT * FROM competitions;
	
	# Métodos úteis:
	# Competition.objects.filter()
	# Competition.objects.order_by()
	# Competition.objects.create(...)
	
	# Competition.objects.filter(datetime__gt=timezone.now()).order_by("subscription_price")
	
	# Devolve a página para o usuário
	return render(
		request, 
		"competitions/list_competition.html", # Template
		{
			"competitions": competitions, 
			"title": "Lista de competições"
		} # Variáveis
	)

	
class CompetitionView(ListView):
	model = Competition

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context["title"] = "Lista de competições"
		return context
