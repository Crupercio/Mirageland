from django.db import IntegrityError
from django.test import TestCase

from accounts.models import User
from catalogue.models import Character, Variant, VariantRarity, VariantSceneType
from collection.models import OwnedVariant
from collection.services import ensure_display_room, place_owned_variant, toggle_room_reaction, update_room_theme


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

    def test_display_room_is_created_with_default_slots(self):
        room = ensure_display_room(self.user)

        self.assertEqual(room.theme_slug, "warm-library")
        self.assertEqual(room.slots.count(), 6)

    def test_placing_variant_moves_it_between_slots(self):
        owned_variant = OwnedVariant.objects.create(user=self.user, variant=self.variant)
        room = ensure_display_room(self.user)

        place_owned_variant(self.user, slot_index=1, owned_variant_id=owned_variant.id)
        place_owned_variant(self.user, slot_index=3, owned_variant_id=owned_variant.id)

        room.refresh_from_db()
        self.assertIsNone(room.slots.get(slot_index=1).owned_variant)
        self.assertEqual(room.slots.get(slot_index=3).owned_variant, owned_variant)

    def test_room_visibility_can_be_updated(self):
        room = ensure_display_room(self.user)
        room.is_public = True
        room.save(update_fields=["is_public"])

        room.refresh_from_db()
        self.assertTrue(room.is_public)

    def test_room_theme_can_be_updated(self):
        room = ensure_display_room(self.user)
        update_room_theme(self.user, "city-loft")

        room.refresh_from_db()
        self.assertEqual(room.theme_slug, "city-loft")

    def test_room_reaction_toggles_from_session_state(self):
        room = ensure_display_room(self.user)
        room.is_public = True
        room.save(update_fields=["is_public"])
        session = {}

        reacted = toggle_room_reaction(room, session)
        room.refresh_from_db()
        self.assertTrue(reacted)
        self.assertEqual(room.reaction_count, 1)

        reacted = toggle_room_reaction(room, session)
        room.refresh_from_db()
        self.assertFalse(reacted)
        self.assertEqual(room.reaction_count, 0)
