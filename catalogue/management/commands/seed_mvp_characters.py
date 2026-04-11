from copy import deepcopy

from django.core.management.base import BaseCommand

from catalogue.models import Character, Variant, VariantRarity, VariantSceneType


MVP_CHARACTERS = [
    {
        "slug": "sora-kasumi",
        "name": "Sora Kasumi",
        "archetype": "The Scholar / Gentle Dreamer",
        "short_description": (
            "A quietly passionate archivist whose curiosity makes her the ideal "
            "first guide into Mirageland."
        ),
        "lore_quote": "Some memories only appear when you sit with them.",
        "color_hex": "#7B5EA7",
        "variants": [
            {
                "slug": "sora-base",
                "name": "Sora Base",
                "scene_type": VariantSceneType.BASE,
                "unlock_order": 1,
                "rarity": VariantRarity.STANDARD,
                "short_description": "Sora stands in the library atrium with an open book glowing softly.",
                "model_file_path": "models/characters/sora/base.glb",
            },
            {
                "slug": "sora-school",
                "name": "Sora School",
                "scene_type": VariantSceneType.SCHOOL,
                "unlock_order": 2,
                "rarity": VariantRarity.STORY,
                "short_description": "Sora studies beside a classroom window, notebook open to hurried notes.",
                "model_file_path": "models/characters/sora/school.glb",
            },
            {
                "slug": "sora-rainy-day",
                "name": "Sora Rainy Day",
                "scene_type": VariantSceneType.RAINY_DAY,
                "unlock_order": 3,
                "rarity": VariantRarity.STORY,
                "short_description": "Sora rests beside a rain-streaked cafe window, wrapped in quiet warmth.",
                "model_file_path": "models/characters/sora/rainy-day.glb",
            },
        ],
    },
    {
        "slug": "ren-takahashi",
        "name": "Ren Takahashi",
        "archetype": "The Rival / Hidden Heart",
        "short_description": (
            "A sharp-edged protector who acts uninterested until the moment "
            "someone needs him."
        ),
        "lore_quote": "Staying doesn't have to look soft to still count.",
        "color_hex": "#445C8C",
        "variants": [
            {
                "slug": "ren-base",
                "name": "Ren Base",
                "scene_type": VariantSceneType.BASE,
                "unlock_order": 1,
                "rarity": VariantRarity.STANDARD,
                "short_description": "Ren waits at a city corner, jacket collar up, watching more than he admits.",
                "model_file_path": "models/characters/ren/base.glb",
            },
            {
                "slug": "ren-school",
                "name": "Ren School",
                "scene_type": VariantSceneType.SCHOOL,
                "unlock_order": 2,
                "rarity": VariantRarity.STORY,
                "short_description": "Ren eats lunch on the rooftop, pretending he wanted the quiet all along.",
                "model_file_path": "models/characters/ren/school.glb",
            },
            {
                "slug": "ren-rainy-day",
                "name": "Ren Rainy Day",
                "scene_type": VariantSceneType.RAINY_DAY,
                "unlock_order": 3,
                "rarity": VariantRarity.STORY,
                "short_description": "Ren waits at a bus stop in the rain, umbrella present but pointedly unused.",
                "model_file_path": "models/characters/ren/rainy-day.glb",
            },
        ],
    },
    {
        "slug": "mei-huang",
        "name": "Mei Huang",
        "archetype": "The Sunshine / Secretly Struggling",
        "short_description": (
            "A bright, affectionate spark whose warmth hides just how hard she works "
            "to be unforgettable."
        ),
        "lore_quote": "If I make the moment bright enough, maybe nobody loses it.",
        "color_hex": "#D89A2B",
        "variants": [
            {
                "slug": "mei-base",
                "name": "Mei Base",
                "scene_type": VariantSceneType.BASE,
                "unlock_order": 1,
                "rarity": VariantRarity.STANDARD,
                "short_description": "Mei waves from a doorway mid-laugh, energy spilling into the room ahead of her.",
                "model_file_path": "models/characters/mei/base.glb",
            },
            {
                "slug": "mei-school",
                "name": "Mei School",
                "scene_type": VariantSceneType.SCHOOL,
                "unlock_order": 2,
                "rarity": VariantRarity.STORY,
                "short_description": "Mei leans over a chalkboard sketching something delightfully off-topic.",
                "model_file_path": "models/characters/mei/school.glb",
            },
            {
                "slug": "mei-rainy-day",
                "name": "Mei Rainy Day",
                "scene_type": VariantSceneType.RAINY_DAY,
                "unlock_order": 3,
                "rarity": VariantRarity.STORY,
                "short_description": "Mei sits quietly beneath yellow light, letting the room hear a softer side of her.",
                "model_file_path": "models/characters/mei/rainy-day.glb",
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the MVP catalogue roster with Sora, Ren, and Mei."

    def handle(self, *args, **options):
        for character_payload in MVP_CHARACTERS:
            data = deepcopy(character_payload)
            variants = data.pop("variants")
            character, _ = Character.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )

            for variant_data in variants:
                Variant.objects.update_or_create(
                    character=character,
                    slug=variant_data["slug"],
                    defaults=variant_data,
                )

        self.stdout.write(self.style.SUCCESS("Seeded the MVP catalogue roster."))
