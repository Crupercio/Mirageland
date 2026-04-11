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
