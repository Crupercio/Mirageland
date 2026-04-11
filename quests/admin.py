from django.contrib import admin

from .models import PlayerQuest, Quest


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ("quest_order", "title", "reward_variant", "reward_coins", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description", "slug")
    ordering = ("quest_order",)


@admin.register(PlayerQuest)
class PlayerQuestAdmin(admin.ModelAdmin):
    list_display = ("user", "quest", "status", "started_at", "completed_at")
    list_filter = ("status", "quest")
    search_fields = ("user__username", "quest__title")
    ordering = ("quest__quest_order",)
