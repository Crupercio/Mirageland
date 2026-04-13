from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from catalogue.models import Character, Variant, VariantRarity, VariantSceneType
from collection.models import OwnedVariant
from collection.services import (
    ensure_display_room,
    get_or_create_variant_customization,
    move_room_slot_variant,
    place_owned_variant,
    reset_variant_customization,
    toggle_room_reaction,
    unlock_room_slot,
    update_variant_render_mode,
    update_room_theme,
)


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
        self.variant_two = Variant.objects.create(
            character=self.character,
            name="Sora School",
            scene_type=VariantSceneType.SCHOOL,
            unlock_order=2,
            rarity=VariantRarity.STORY,
            short_description="Sora in a quiet school memory.",
            model_file_path="models/characters/sora/school.glb",
        )

    def test_user_cannot_own_same_variant_twice(self):
        OwnedVariant.objects.create(user=self.user, variant=self.variant)

        with self.assertRaises(IntegrityError):
            OwnedVariant.objects.create(user=self.user, variant=self.variant)

    def test_display_room_is_created_with_default_slots(self):
        room = ensure_display_room(self.user)

        self.assertEqual(room.theme_slug, "warm-library")
        self.assertEqual(room.slots.count(), 10)
        self.assertEqual(room.slots.filter(is_unlocked=True).count(), 1)
        self.assertTrue(room.slots.get(slot_index=2).is_unlocked)

    def test_placing_variant_moves_it_between_slots(self):
        owned_variant = OwnedVariant.objects.create(user=self.user, variant=self.variant)
        room = ensure_display_room(self.user)
        room.slots.filter(slot_index__in=[1, 3]).update(is_unlocked=True)

        place_owned_variant(self.user, slot_index=1, owned_variant_id=owned_variant.id)
        place_owned_variant(self.user, slot_index=3, owned_variant_id=owned_variant.id)

        room.refresh_from_db()
        self.assertIsNone(room.slots.get(slot_index=1).owned_variant)
        self.assertEqual(room.slots.get(slot_index=3).owned_variant, owned_variant)

    def test_locked_slot_cannot_receive_variant(self):
        owned_variant = OwnedVariant.objects.create(user=self.user, variant=self.variant)
        ensure_display_room(self.user)

        with self.assertRaises(ValueError):
            place_owned_variant(self.user, slot_index=1, owned_variant_id=owned_variant.id)

    def test_drag_move_transfers_variant_to_empty_slot(self):
        owned_variant = OwnedVariant.objects.create(user=self.user, variant=self.variant)
        room = ensure_display_room(self.user)
        room.slots.filter(slot_index__in=[1, 3]).update(is_unlocked=True)
        place_owned_variant(self.user, slot_index=1, owned_variant_id=owned_variant.id)

        move_room_slot_variant(self.user, from_slot_index=1, to_slot_index=3)

        room.refresh_from_db()
        self.assertIsNone(room.slots.get(slot_index=1).owned_variant)
        self.assertEqual(room.slots.get(slot_index=3).owned_variant, owned_variant)

    def test_drag_move_swaps_two_occupied_slots(self):
        owned_variant_one = OwnedVariant.objects.create(user=self.user, variant=self.variant)
        owned_variant_two = OwnedVariant.objects.create(user=self.user, variant=self.variant_two)
        room = ensure_display_room(self.user)
        room.slots.filter(slot_index__in=[1, 3]).update(is_unlocked=True)
        place_owned_variant(self.user, slot_index=1, owned_variant_id=owned_variant_one.id)
        place_owned_variant(self.user, slot_index=3, owned_variant_id=owned_variant_two.id)

        move_room_slot_variant(self.user, from_slot_index=1, to_slot_index=3)

        room.refresh_from_db()
        self.assertEqual(room.slots.get(slot_index=1).owned_variant, owned_variant_two)
        self.assertEqual(room.slots.get(slot_index=3).owned_variant, owned_variant_one)

    def test_unlock_slot_spends_coins(self):
        self.user.coins = 20
        self.user.save(update_fields=["coins"])
        room = ensure_display_room(self.user)

        unlocked_slot = unlock_room_slot(self.user, slot_index=1)
        self.user.refresh_from_db()
        room.refresh_from_db()

        self.assertTrue(unlocked_slot.is_unlocked)
        self.assertEqual(self.user.coins, 5)
        self.assertTrue(room.slots.get(slot_index=1).is_unlocked)

    def test_second_shelf_center_requires_first_shelf_progress(self):
        self.user.coins = 100
        self.user.save(update_fields=["coins"])
        ensure_display_room(self.user)

        with self.assertRaises(ValueError):
            unlock_room_slot(self.user, slot_index=5)

        unlock_room_slot(self.user, slot_index=1)
        unlock_room_slot(self.user, slot_index=3)
        unlocked_slot = unlock_room_slot(self.user, slot_index=5)

        self.assertTrue(unlocked_slot.is_unlocked)

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

    def test_render_mode_customization_defaults_to_normal(self):
        owned_variant = OwnedVariant.objects.create(user=self.user, variant=self.variant)

        customization_state = get_or_create_variant_customization(owned_variant)

        self.assertEqual(customization_state.render_mode, "normal")
        self.assertEqual(customization_state.hidden_parts, [])
        self.assertEqual(customization_state.morph_values, {})

    def test_render_mode_customization_can_be_updated_and_reset(self):
        owned_variant = OwnedVariant.objects.create(user=self.user, variant=self.variant)

        customization_state = update_variant_render_mode(self.user, owned_variant.id, "wireframe")
        self.assertEqual(customization_state.render_mode, "wireframe")

        customization_state = reset_variant_customization(self.user, owned_variant.id)
        self.assertEqual(customization_state.render_mode, "normal")
        self.assertEqual(customization_state.hidden_parts, [])
        self.assertEqual(customization_state.morph_values, {})

    def test_room_detail_exposes_saved_render_mode_for_scene_slots(self):
        owned_variant = OwnedVariant.objects.create(user=self.user, variant=self.variant)
        room = ensure_display_room(self.user)
        room.slots.filter(slot_index=2).update(owned_variant=owned_variant)
        update_variant_render_mode(self.user, owned_variant.id, "unlit")
        self.client.force_login(self.user)

        response = self.client.get(reverse("collection:room-detail"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-render-mode="unlit"')
