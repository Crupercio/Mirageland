from django.core.management.base import BaseCommand

from catalogue.asset_profiles import build_variant_asset_profile
from catalogue.models import Variant


class Command(BaseCommand):
    help = "Generate immutable asset profiles for variant GLB files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--character-slug",
            dest="character_slug",
            help="Only build profiles for variants belonging to this character slug.",
        )

    def handle(self, *args, **options):
        variants = Variant.objects.select_related("character").order_by(
            "character__name", "unlock_order", "name"
        )
        if options.get("character_slug"):
            variants = variants.filter(character__slug=options["character_slug"])

        count = 0
        for variant in variants:
            profile = build_variant_asset_profile(variant)
            count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Built profile for {variant.character.name} / {variant.name} "
                    f"({len(profile.parts_schema)} parts, "
                    f"{len(profile.morph_schema)} morphs, "
                    f"{len(profile.animation_schema)} animations)"
                )
            )

        if count == 0:
            self.stdout.write(self.style.WARNING("No variants matched the requested scope."))
