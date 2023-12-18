from django.contrib import admin
from .models import Sport, Modality


class ModalityInline(admin.TabularInline):
    model = Modality
    extra = 1


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    inlines = [ModalityInline]
