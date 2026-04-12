from django.core.management.base import BaseCommand, CommandError

from catalogue.models import Variant
from quests.models import Quest


class Command(BaseCommand):
    help = "Seed the first three story chapters for Sora, Ren, and Mei."

    def handle(self, *args, **options):
        try:
            base_variant = Variant.objects.get(slug="sora-base")
            school_variant = Variant.objects.get(slug="sora-school")
            rainy_day_variant = Variant.objects.get(slug="sora-rainy-day")
            ren_base_variant = Variant.objects.get(slug="ren-base")
            ren_school_variant = Variant.objects.get(slug="ren-school")
            ren_rainy_day_variant = Variant.objects.get(slug="ren-rainy-day")
            mei_base_variant = Variant.objects.get(slug="mei-base")
            mei_school_variant = Variant.objects.get(slug="mei-school")
            mei_rainy_day_variant = Variant.objects.get(slug="mei-rainy-day")
        except Variant.DoesNotExist as exc:
            raise CommandError(
                "Required MVP variants are missing. Run `python manage.py seed_mvp_characters` first."
            ) from exc

        quests = [
            {
                "slug": "first-light",
                "title": "First Light",
                "description": (
                    "Meet Sora, step into Mirageland, and receive the first figurine."
                ),
                "chapter_number": 1,
                "chapter_title": "Chapter 1 - First Light",
                "quest_order": 1,
                "reward_variant": base_variant,
                "reward_coins": 0,
            },
            {
                "slug": "margin-notes",
                "title": "Margin Notes",
                "description": (
                    "Revisit Sora's story and unlock the classroom memory she shares next."
                ),
                "chapter_number": 1,
                "chapter_title": "Chapter 1 - First Light",
                "quest_order": 2,
                "reward_variant": school_variant,
                "reward_coins": 15,
            },
            {
                "slug": "shelf-memory",
                "title": "Shelf Memory",
                "description": (
                    "Place Sora within your collection mindset and deepen the sense of ownership."
                ),
                "chapter_number": 1,
                "chapter_title": "Chapter 1 - First Light",
                "quest_order": 3,
                "reward_variant": None,
                "reward_coins": 25,
            },
            {
                "slug": "quiet-hours",
                "title": "Quiet Hours",
                "description": (
                    "Return to Sora after the earlier moments settle and unlock her rainy-day variant."
                ),
                "chapter_number": 1,
                "chapter_title": "Chapter 1 - First Light",
                "quest_order": 4,
                "reward_variant": rainy_day_variant,
                "reward_coins": 20,
            },
            {
                "slug": "street-corner-promise",
                "title": "Street Corner Promise",
                "description": (
                    "Follow the next pull in Mirageland and meet Ren at the edge of a city-night memory."
                ),
                "chapter_number": 2,
                "chapter_title": "Chapter 2 - Sharp Edges",
                "quest_order": 5,
                "reward_variant": ren_base_variant,
                "reward_coins": 10,
            },
            {
                "slug": "rooftop-static",
                "title": "Rooftop Static",
                "description": (
                    "Stay with Ren long enough for the quieter school version of his story to surface."
                ),
                "chapter_number": 2,
                "chapter_title": "Chapter 2 - Sharp Edges",
                "quest_order": 6,
                "reward_variant": ren_school_variant,
                "reward_coins": 15,
            },
            {
                "slug": "storm-signal",
                "title": "Storm Signal",
                "description": (
                    "See Ren through the rain-soaked chapter close and claim the final variant from his arc."
                ),
                "chapter_number": 2,
                "chapter_title": "Chapter 2 - Sharp Edges",
                "quest_order": 7,
                "reward_variant": ren_rainy_day_variant,
                "reward_coins": 20,
            },
            {
                "slug": "open-door-laughter",
                "title": "Open Door Laughter",
                "description": (
                    "Step into Mei's brighter orbit and claim the first spark of her chapter."
                ),
                "chapter_number": 3,
                "chapter_title": "Chapter 3 - Golden Echoes",
                "quest_order": 8,
                "reward_variant": mei_base_variant,
                "reward_coins": 10,
            },
            {
                "slug": "chalkline-sun",
                "title": "Chalkline Sun",
                "description": (
                    "Stay with Mei through the loud classroom warmth that hides how much she carries."
                ),
                "chapter_number": 3,
                "chapter_title": "Chapter 3 - Golden Echoes",
                "quest_order": 9,
                "reward_variant": mei_school_variant,
                "reward_coins": 15,
            },
            {
                "slug": "lampglow-kept",
                "title": "Lampglow Kept",
                "description": (
                    "Follow Mei into her quieter rainy-night moment and unlock the final chapter reward."
                ),
                "chapter_number": 3,
                "chapter_title": "Chapter 3 - Golden Echoes",
                "quest_order": 10,
                "reward_variant": mei_rainy_day_variant,
                "reward_coins": 20,
            },
        ]

        for quest_data in quests:
            Quest.objects.update_or_create(
                slug=quest_data["slug"],
                defaults=quest_data,
            )

        self.stdout.write(self.style.SUCCESS("Seeded Mirageland Chapter 1 through Chapter 3 quests."))
