from django.conf import settings
from django.db import models

from catalogue.models import Variant


class OwnedVariant(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_variants",
    )
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name="owners",
    )
    acquired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["variant__character__name", "variant__unlock_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "variant"],
                name="unique_owned_variant_per_user",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} owns {self.variant}"


class DisplayRoom(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="display_room",
    )
    theme_slug = models.SlugField(max_length=100, default="warm-library")
    is_public = models.BooleanField(default=False)
    reaction_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self) -> str:
        return f"{self.user.username}'s room"


class ShelfSlot(models.Model):
    room = models.ForeignKey(
        DisplayRoom,
        on_delete=models.CASCADE,
        related_name="slots",
    )
    slot_index = models.PositiveSmallIntegerField()
    shelf_index = models.PositiveSmallIntegerField(default=1)
    slot_code = models.CharField(max_length=12, default="c")
    display_order = models.PositiveSmallIntegerField(default=1)
    is_unlocked = models.BooleanField(default=False)
    unlock_cost = models.PositiveIntegerField(default=0)
    owned_variant = models.OneToOneField(
        OwnedVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shelf_slot",
    )

    class Meta:
        ordering = ["room", "shelf_index", "display_order", "slot_index"]
        constraints = [
            models.UniqueConstraint(
                fields=["room", "slot_index"],
                name="unique_slot_index_per_room",
            ),
            models.UniqueConstraint(
                fields=["room", "shelf_index", "slot_code"],
                name="unique_slot_code_per_shelf",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.room.user.username} shelf {self.shelf_index} {self.slot_code}"
