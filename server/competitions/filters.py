import django_filters
from .models import Modality, Competition
from sports.models import Sport

class CompetitionFilter(django_filters.FilterSet):
  modality = django_filters.ModelChoiceFilter(queryset=Modality.objects.all(), label='Modalidade')
  sport = django_filters.ModelChoiceFilter(queryset=Sport.objects.all(), label='Esporte', field_name='modality__sport')

  subscription_price = django_filters.NumberFilter()
  subscription_price__lt = django_filters.NumberFilter(field_name='subscription_price', lookup_expr='lt')
  subscription_price__gt = django_filters.NumberFilter(field_name='subscription_price', lookup_expr='gt')

  max_slots = django_filters.NumberFilter()
  max_slots__lt = django_filters.NumberFilter(field_name='max_slots', lookup_expr='lt')
  max_slots__gt = django_filters.NumberFilter(field_name='max_slots', lookup_expr='gt')

  city = django_filters.CharFilter(lookup_expr='icontains', label='Cidade')
  state = django_filters.CharFilter(lookup_expr='icontains', label='Estado')


  class Meta:
    model = Competition
    fields = ['datetime', 'city', 'state', 'subscription_price', 'max_slots']
