from django.core.management.base import BaseCommand, CommandError

from catalogue.models import Variant
from quests.models import Quest


class Command(BaseCommand):
    help = "Seed the four Sora vertical-slice quests."

    def handle(self, *args, **options):
        try:
            base_variant = Variant.objects.get(slug="sora-base")
            school_variant = Variant.objects.get(slug="sora-school")
            rainy_day_variant = Variant.objects.get(slug="sora-rainy-day")
        except Variant.DoesNotExist as exc:
            raise CommandError(
                "Sora variants are missing. Run `python manage.py seed_sora_slice` first."
            ) from exc

        quests = [
            {
                "slug": "first-light",
                "title": "First Light",
                "description": (
                    "Meet Sora, step into Mirageland, and receive the first figurine."
                ),
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
                "quest_order": 4,
                "reward_variant": rainy_day_variant,
                "reward_coins": 20,
            },
        ]

        for quest_data in quests:
            Quest.objects.update_or_create(
                slug=quest_data["slug"],
                defaults=quest_data,
            )

        self.stdout.write(self.style.SUCCESS("Seeded Sora quest chain."))
