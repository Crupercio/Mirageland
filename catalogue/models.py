from django.db import models
from django.utils.text import slugify


class VariantSceneType(models.TextChoices):
    BASE = "base", "Base"
    SCHOOL = "school", "School"
    RAINY_DAY = "rainy_day", "Rainy Day"


class VariantRarity(models.TextChoices):
    STANDARD = "standard", "Standard"
    STORY = "story", "Story"


class Character(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    archetype = models.CharField(max_length=100)
    short_description = models.TextField()
    lore_quote = models.CharField(max_length=255)
    color_hex = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Variant(models.Model):
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="variants",
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    scene_type = models.CharField(max_length=32, choices=VariantSceneType.choices)
    unlock_order = models.PositiveSmallIntegerField()
    rarity = models.CharField(
        max_length=32,
        choices=VariantRarity.choices,
        default=VariantRarity.STANDARD,
    )
    short_description = models.TextField()
    model_file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["character__name", "unlock_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["character", "slug"],
                name="unique_variant_slug_per_character",
            ),
            models.UniqueConstraint(
                fields=["character", "scene_type"],
                name="unique_variant_scene_per_character",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.character.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
