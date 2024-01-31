from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import User, OrganizerRequest


class CustomUserAdmin(UserAdmin):
    fieldsets = fieldsets = (
        (None, {"fields": ("username", "cpf", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "cpf", "password1", "password2"),
            },
        ),
    )
    list_display = ["username", "email", "first_name", "last_name", "is_staff"]

class OrganizerRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']
    actions = ['accept_organizer_request', 'decline_organizer_request']

    def accept_organizer_request(self, request, queryset):
        for request in queryset:
            user = request.user
            user.is_organizer = True
            user.save()

            # Update the status of the OrganizerRequest
            request.status = 'Aceito'
            request.save()

    accept_organizer_request.short_description = "Aceitar os pedidos selecionados"

    def decline_organizer_request(self, request, queryset):
        for request in queryset:
            request.status = 'Recusado'
            request.save()

    decline_organizer_request.short_description = "Recusar os pedidos selecionados"

admin.site.register(User, CustomUserAdmin)
admin.site.register(OrganizerRequest, OrganizerRequestAdmin)

