from django.contrib import admin

from .models import Competition, CompetitionRate, CompetitionSubscription


admin.site.register(Competition)
admin.site.register(CompetitionSubscription)


@admin.register(CompetitionRate)
class CompetitionRateAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "competition", "rating")
    list_filter = ("rating",)
    search_fields = ("competition",)
