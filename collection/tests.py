from django.db import IntegrityError
from django.test import TestCase

from accounts.models import User
from catalogue.models import Character, Variant, VariantRarity, VariantSceneType
from collection.models import OwnedVariant


class OwnedVariantModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="collector", password="testpass123")
        self.character = Character.objects.create(
            name="Sora Kasumi",
            archetype="The Scholar / Gentle Dreamer",
            short_description="A soft-spoken archivist drawn to the Prism Effect.",
            lore_quote="Some memories only appear when you sit with them.",
            color_hex="#7B5EA7",
        )
        self.variant = Variant.objects.create(
            character=self.character,
            name="Sora Base",
            scene_type=VariantSceneType.BASE,
            unlock_order=1,
            rarity=VariantRarity.STANDARD,
            short_description="Sora in the library atrium.",
            model_file_path="models/characters/sora/base.glb",
        )

    def test_user_cannot_own_same_variant_twice(self):
        OwnedVariant.objects.create(user=self.user, variant=self.variant)

        with self.assertRaises(IntegrityError):
            OwnedVariant.objects.create(user=self.user, variant=self.variant)
