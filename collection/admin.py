from django.contrib import admin

from .models import DisplayRoom, OwnedVariant, ShelfSlot


@admin.register(OwnedVariant)
class OwnedVariantAdmin(admin.ModelAdmin):
    list_display = ("user", "variant", "acquired_at")
    list_filter = ("variant__character", "variant__scene_type")
    search_fields = ("user__username", "variant__name", "variant__character__name")


class ShelfSlotInline(admin.TabularInline):
    model = ShelfSlot
    extra = 0


@admin.register(DisplayRoom)
class DisplayRoomAdmin(admin.ModelAdmin):
    list_display = ("user", "theme_slug", "is_public", "updated_at")
    list_filter = ("theme_slug", "is_public")
    search_fields = ("user__username",)
    inlines = [ShelfSlotInline]


@admin.register(ShelfSlot)
class ShelfSlotAdmin(admin.ModelAdmin):
    list_display = ("room", "slot_index", "owned_variant")
    list_filter = ("room__theme_slug",)
    search_fields = ("room__user__username", "owned_variant__variant__name")
