from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class MiragelandUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Mirageland", {"fields": ("coins",)}),
    )
    list_display = ("username", "email", "is_staff", "coins")

