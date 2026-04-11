from django.contrib import admin

from .models import OwnedVariant


@admin.register(OwnedVariant)
class OwnedVariantAdmin(admin.ModelAdmin):
    list_display = ("user", "variant", "acquired_at")
    list_filter = ("variant__character", "variant__scene_type")
    search_fields = ("user__username", "variant__name", "variant__character__name")
