from django.contrib import admin

from .models import (
    Competition,
    CompetitionRate,
    CompetitionSubscription,
    CompetitionDocument,
    OrganizerRequest,
    CompetitionResults,
    OrganizerRequestStatus,
)


admin.site.register(Competition)
admin.site.register(CompetitionSubscription)
admin.site.register(CompetitionDocument)
admin.site.register(CompetitionResults)


@admin.register(CompetitionRate)
class CompetitionRateAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "competition", "rating")
    list_filter = ("rating",)
    search_fields = ("competition",)


@admin.register(OrganizerRequest)
class OrganizerRequestAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "status", "created_at")
    list_filter = ("status",)

    def save_model(self, request, obj, form, change) -> None:
        if not change:
            return super().save_model(request, obj, form, change)

        if obj.status == OrganizerRequestStatus.APPROVED:
            obj.approve()
        elif obj.status == OrganizerRequestStatus.REJECTED:
            obj.reject()
        return super().save_model(request, obj, form, change)
