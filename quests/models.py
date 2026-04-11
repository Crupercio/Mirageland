from django.conf import settings
from django.db import models

from catalogue.models import Variant


class PlayerQuestStatus(models.TextChoices):
    LOCKED = "locked", "Locked"
    AVAILABLE = "available", "Available"
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"


class Quest(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    quest_order = models.PositiveSmallIntegerField(unique=True)
    reward_variant = models.ForeignKey(
        Variant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rewarding_quests",
    )
    reward_coins = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["quest_order", "id"]

    def __str__(self) -> str:
        return self.title


class PlayerQuest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="player_quests",
    )
    quest = models.ForeignKey(
        Quest,
        on_delete=models.CASCADE,
        related_name="player_states",
    )
    status = models.CharField(
        max_length=16,
        choices=PlayerQuestStatus.choices,
        default=PlayerQuestStatus.LOCKED,
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["quest__quest_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "quest"],
                name="unique_player_quest_per_user",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username}: {self.quest.title} ({self.status})"
