from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import User


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
    list_display = ["username", "cpf", "email", "first_name", "last_name", "is_staff"]


admin.site.register(User, CustomUserAdmin)
