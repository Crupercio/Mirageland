from django.db import IntegrityError
from django.test import TestCase

from accounts.models import User
from collection.models import OwnedVariant

from .models import Character, Variant, VariantRarity, VariantSceneType


class CharacterModelTests(TestCase):
    def test_character_generates_slug(self):
        character = Character.objects.create(
            name="Sora Kasumi",
            archetype="The Scholar / Gentle Dreamer",
            short_description="A soft-spoken archivist drawn to the Prism Effect.",
            lore_quote="Some memories only appear when you sit with them.",
            color_hex="#7B5EA7",
        )

        self.assertEqual(character.slug, "sora-kasumi")


class VariantModelTests(TestCase):
    def setUp(self):
        self.character = Character.objects.create(
            name="Sora Kasumi",
            archetype="The Scholar / Gentle Dreamer",
            short_description="A soft-spoken archivist drawn to the Prism Effect.",
            lore_quote="Some memories only appear when you sit with them.",
            color_hex="#7B5EA7",
        )

    def test_variant_generates_slug(self):
        variant = Variant.objects.create(
            character=self.character,
            name="Sora Rainy Day",
            scene_type=VariantSceneType.RAINY_DAY,
            unlock_order=3,
            rarity=VariantRarity.STORY,
            short_description="Sora sits beside a rain-washed cafe window.",
            model_file_path="models/characters/sora/rainy-day.glb",
        )

        self.assertEqual(variant.slug, "sora-rainy-day")

    def test_scene_type_is_unique_per_character(self):
        Variant.objects.create(
            character=self.character,
            name="Sora Base",
            scene_type=VariantSceneType.BASE,
            unlock_order=1,
            rarity=VariantRarity.STANDARD,
            short_description="Sora in the library atrium.",
            model_file_path="models/characters/sora/base.glb",
        )

        with self.assertRaises(IntegrityError):
            Variant.objects.create(
                character=self.character,
                name="Sora Base Alternate",
                scene_type=VariantSceneType.BASE,
                unlock_order=99,
                rarity=VariantRarity.STANDARD,
                short_description="A duplicate base scene should not exist.",
                model_file_path="models/characters/sora/base-alt.glb",
            )


class CharacterDetailViewTests(TestCase):
    def setUp(self):
        self.collector = User.objects.create_user(
            username="demo_collector",
            password="testpass123",
        )
        self.character = Character.objects.create(
            name="Sora Kasumi",
            archetype="The Scholar / Gentle Dreamer",
            short_description="A soft-spoken archivist drawn to the Prism Effect.",
            lore_quote="Some memories only appear when you sit with them.",
            color_hex="#7B5EA7",
        )
        self.base_variant = Variant.objects.create(
            character=self.character,
            name="Sora Base",
            scene_type=VariantSceneType.BASE,
            unlock_order=1,
            rarity=VariantRarity.STANDARD,
            short_description="Sora in the library atrium.",
            model_file_path="models/characters/sora/base.glb",
        )
        self.school_variant = Variant.objects.create(
            character=self.character,
            name="Sora School",
            scene_type=VariantSceneType.SCHOOL,
            unlock_order=2,
            rarity=VariantRarity.STORY,
            short_description="Sora beside a classroom window.",
            model_file_path="models/characters/sora/school.glb",
        )
        OwnedVariant.objects.create(user=self.collector, variant=self.base_variant)

    def test_character_detail_renders(self):
        response = self.client.get(f"/catalogue/characters/{self.character.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sora Kasumi")
        self.assertContains(response, "Sora Base")
        self.assertContains(response, "Owned")
