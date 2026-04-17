from django.contrib import admin

from .models import Character, Variant, VariantAssetProfile


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


@admin.register(VariantAssetProfile)
class VariantAssetProfileAdmin(admin.ModelAdmin):
    list_display = ("variant", "asset_version", "generated_at")
    search_fields = ("variant__name", "variant__character__name")
    readonly_fields = ("generated_at",)
