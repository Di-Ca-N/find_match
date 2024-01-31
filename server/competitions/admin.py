from django.contrib import admin

from .models import Competition, CompetitionRate


admin.site.register(Competition)


@admin.register(CompetitionRate)
class CompetitionRateAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "competition", "rating")
    list_filter = ("rating",)
    search_fields = ("competition",)
