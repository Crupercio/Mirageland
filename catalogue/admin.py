from django.contrib import admin

from .models import Character, Variant


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "archetype", "slug", "created_at")
    search_fields = ("name", "archetype", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [VariantInline]


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ("name", "character", "scene_type", "rarity", "unlock_order")
    list_filter = ("scene_type", "rarity", "character")
    search_fields = ("name", "character__name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
