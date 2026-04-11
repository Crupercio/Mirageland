from django.core.management.base import BaseCommand

from catalogue.models import Character, Variant, VariantRarity, VariantSceneType


class Command(BaseCommand):
    help = "Seed Sora Kasumi and her three vertical-slice variants."

    def handle(self, *args, **options):
        character, created = Character.objects.update_or_create(
            slug="sora-kasumi",
            defaults={
                "name": "Sora Kasumi",
                "archetype": "The Scholar / Gentle Dreamer",
                "short_description": (
                    "A quietly passionate archivist whose curiosity makes her "
                    "the ideal first guide into Mirageland."
                ),
                "lore_quote": "Some memories only appear when you sit with them.",
                "color_hex": "#7B5EA7",
            },
        )

        variants = [
            {
                "slug": "sora-base",
                "name": "Sora Base",
                "scene_type": VariantSceneType.BASE,
                "unlock_order": 1,
                "rarity": VariantRarity.STANDARD,
                "short_description": (
                    "Sora stands in the library atrium with an open book glowing softly."
                ),
                "model_file_path": "models/characters/sora/base.glb",
            },
            {
                "slug": "sora-school",
                "name": "Sora School",
                "scene_type": VariantSceneType.SCHOOL,
                "unlock_order": 2,
                "rarity": VariantRarity.STORY,
                "short_description": (
                    "Sora studies beside a classroom window, notebook open to hurried notes."
                ),
                "model_file_path": "models/characters/sora/school.glb",
            },
            {
                "slug": "sora-rainy-day",
                "name": "Sora Rainy Day",
                "scene_type": VariantSceneType.RAINY_DAY,
                "unlock_order": 3,
                "rarity": VariantRarity.STORY,
                "short_description": (
                    "Sora rests beside a rain-streaked cafe window, wrapped in quiet warmth."
                ),
                "model_file_path": "models/characters/sora/rainy-day.glb",
            },
        ]

        for variant_data in variants:
            Variant.objects.update_or_create(
                character=character,
                slug=variant_data["slug"],
                defaults=variant_data,
            )

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} Sora slice data."))
