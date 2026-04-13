from django.db import IntegrityError
from django.test import TestCase

from accounts.models import User
from collection.models import OwnedVariant, OwnedVariantCustomization, OwnedVariantRenderMode

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
        self.client.force_login(self.collector)
        response = self.client.get(f"/catalogue/characters/{self.character.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sora Kasumi")
        self.assertContains(response, "Sora Base")
        self.assertContains(response, "Owned")
        self.assertContains(response, 'data-variant-owned="true"')

    def test_character_detail_marks_locked_variant_preview_state(self):
        self.client.force_login(self.collector)
        response = self.client.get(
            f"/catalogue/characters/{self.character.slug}/",
            {"variant": self.school_variant.slug},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sora School")
        self.assertContains(response, 'data-variant-owned="false"')
        self.assertContains(response, "Locked preview")

    def test_character_detail_includes_saved_render_mode_for_owned_variant(self):
        owned_variant = OwnedVariant.objects.get(user=self.collector, variant=self.base_variant)
        OwnedVariantCustomization.objects.create(
            owned_variant=owned_variant,
            render_mode=OwnedVariantRenderMode.UNLIT,
        )

        self.client.force_login(self.collector)
        response = self.client.get(f"/catalogue/characters/{self.character.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-initial-render-mode="unlit"')

    def test_character_detail_redirects_anonymous_collectors_to_login(self):
        response = self.client.get(f"/catalogue/characters/{self.character.slug}/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_render_mode_save_endpoint_updates_owned_variant_state(self):
        owned_variant = OwnedVariant.objects.get(user=self.collector, variant=self.base_variant)
        self.client.force_login(self.collector)

        response = self.client.post(
            "/catalogue/owned-variants/render-mode/",
            {
                "owned_variant_id": owned_variant.id,
                "render_mode": "wireframe",
            },
        )

        self.assertEqual(response.status_code, 200)
        owned_variant.refresh_from_db()
        self.assertEqual(owned_variant.customization_state.render_mode, "wireframe")

    def test_render_mode_save_endpoint_accepts_hidden_parts_and_morph_values(self):
        owned_variant = OwnedVariant.objects.get(user=self.collector, variant=self.base_variant)
        self.client.force_login(self.collector)

        response = self.client.post(
            "/catalogue/owned-variants/render-mode/",
            {
                "owned_variant_id": owned_variant.id,
                "render_mode": "unlit",
                "hidden_parts": '["shoe","socks"]',
                "morph_values": '{"smile": 0.75, "blink": 0.2}',
            },
        )

        self.assertEqual(response.status_code, 200)
        owned_variant.refresh_from_db()
        self.assertEqual(owned_variant.customization_state.render_mode, "unlit")
        self.assertEqual(owned_variant.customization_state.hidden_parts, ["shoe", "socks"])
        self.assertEqual(owned_variant.customization_state.morph_values, {"smile": 0.75, "blink": 0.2})

    def test_render_mode_reset_endpoint_restores_default_state(self):
        owned_variant = OwnedVariant.objects.get(user=self.collector, variant=self.base_variant)
        OwnedVariantCustomization.objects.create(
            owned_variant=owned_variant,
            render_mode=OwnedVariantRenderMode.WIREFRAME,
            hidden_parts=["shoes"],
            morph_values={"smile": 0.4},
        )
        self.client.force_login(self.collector)

        response = self.client.post(
            "/catalogue/owned-variants/reset-state/",
            {
                "owned_variant_id": owned_variant.id,
                "next": f"/catalogue/characters/{self.character.slug}/",
            },
        )

        self.assertEqual(response.status_code, 302)
        owned_variant.refresh_from_db()
        self.assertEqual(owned_variant.customization_state.render_mode, "normal")
        self.assertEqual(owned_variant.customization_state.hidden_parts, [])
        self.assertEqual(owned_variant.customization_state.morph_values, {})

    def test_render_mode_reset_endpoint_returns_json_for_ajax_requests(self):
        owned_variant = OwnedVariant.objects.get(user=self.collector, variant=self.base_variant)
        OwnedVariantCustomization.objects.create(
            owned_variant=owned_variant,
            render_mode=OwnedVariantRenderMode.WIREFRAME,
            hidden_parts=["shoes"],
            morph_values={"smile": 0.4},
        )
        self.client.force_login(self.collector)

        response = self.client.post(
            "/catalogue/owned-variants/reset-state/",
            {
                "owned_variant_id": owned_variant.id,
                "next": f"/catalogue/characters/{self.character.slug}/",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["render_mode"], "normal")
        self.assertEqual(payload["hidden_parts"], [])
        self.assertEqual(payload["morph_values"], {})

    def test_lab_view_loads_saved_hidden_parts_and_morph_values(self):
        owned_variant = OwnedVariant.objects.get(user=self.collector, variant=self.base_variant)
        OwnedVariantCustomization.objects.create(
            owned_variant=owned_variant,
            render_mode=OwnedVariantRenderMode.UNLIT,
            hidden_parts=["shoe"],
            morph_values={"smile": 0.55},
        )
        self.client.force_login(self.collector)

        response = self.client.get(f"/catalogue/lab/?owned_variant={owned_variant.id}")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-initial-render-mode="unlit"')
        self.assertContains(response, 'data-hidden-parts="[\\u0022shoe\\u0022]"')
        self.assertContains(response, 'data-morph-values="{\\u0022smile\\u0022: 0.55}"')

    def test_reset_all_states_endpoint_clears_all_owned_variant_customizations(self):
        owned_variant = OwnedVariant.objects.get(user=self.collector, variant=self.base_variant)
        OwnedVariantCustomization.objects.create(
            owned_variant=owned_variant,
            render_mode=OwnedVariantRenderMode.WIREFRAME,
            hidden_parts=["shoe"],
            morph_values={"smile": 0.55},
        )
        self.client.force_login(self.collector)

        response = self.client.post(
            "/catalogue/owned-variants/reset-all-states/",
            {"next": "/catalogue/lab/"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        owned_variant.refresh_from_db()
        self.assertEqual(owned_variant.customization_state.render_mode, "normal")
        self.assertEqual(owned_variant.customization_state.hidden_parts, [])
        self.assertEqual(owned_variant.customization_state.morph_values, {})


class CatalogueIndexViewTests(TestCase):
    def setUp(self):
        self.collector = User.objects.create_user(
            username="demo_collector",
            password="testpass123",
        )
        self.sora = Character.objects.create(
            name="Sora Kasumi",
            archetype="The Scholar / Gentle Dreamer",
            short_description="A soft-spoken archivist drawn to the Prism Effect.",
            lore_quote="Some memories only appear when you sit with them.",
            color_hex="#7B5EA7",
        )
        self.ren = Character.objects.create(
            name="Ren Takahashi",
            archetype="The Rival / Hidden Heart",
            short_description="A sharp-edged protector who watches from the edge.",
            lore_quote="Staying doesn't have to look soft to still count.",
            color_hex="#445C8C",
        )
        self.sora_variant = Variant.objects.create(
            character=self.sora,
            name="Sora Base",
            scene_type=VariantSceneType.BASE,
            unlock_order=1,
            rarity=VariantRarity.STANDARD,
            short_description="Sora in the library atrium.",
            model_file_path="models/characters/sora/base.glb",
        )
        Variant.objects.create(
            character=self.ren,
            name="Ren Base",
            scene_type=VariantSceneType.BASE,
            unlock_order=1,
            rarity=VariantRarity.STANDARD,
            short_description="Ren on a street corner.",
            model_file_path="models/characters/ren/base.glb",
        )
        OwnedVariant.objects.create(user=self.collector, variant=self.sora_variant)

    def test_catalogue_index_renders_character_progress(self):
        self.client.force_login(self.collector)
        response = self.client.get("/catalogue/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sora Kasumi")
        self.assertContains(response, "Ren Takahashi")
        self.assertContains(response, "1 / 1")

    def test_catalogue_index_redirects_anonymous_collectors_to_login(self):
        response = self.client.get("/catalogue/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])


class CustomizationLabViewTests(TestCase):
    def setUp(self):
        self.collector = User.objects.create_user(
            username="lab_collector",
            password="testpass123",
        )
        self.character = Character.objects.create(
            name="Mei Huang",
            archetype="The Spark / Open Door",
            short_description="A bright presence who keeps the room warm.",
            lore_quote="A little laughter opens more doors than force.",
            color_hex="#D4A04F",
        )
        self.base_variant = Variant.objects.create(
            character=self.character,
            name="Mei Base",
            scene_type=VariantSceneType.BASE,
            unlock_order=1,
            rarity=VariantRarity.STANDARD,
            short_description="Mei with warm collector energy.",
            model_file_path="models/characters/mei/base.glb",
        )
        self.owned_variant = OwnedVariant.objects.create(user=self.collector, variant=self.base_variant)

    def test_lab_requires_login(self):
        response = self.client.get("/catalogue/lab/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_lab_renders_owned_variant_and_saved_state(self):
        OwnedVariantCustomization.objects.create(
            owned_variant=self.owned_variant,
            render_mode=OwnedVariantRenderMode.WIREFRAME,
        )
        self.client.force_login(self.collector)

        response = self.client.get("/catalogue/lab/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Figurine Lab")
        self.assertContains(response, "Mei Base")
        self.assertContains(response, 'data-initial-render-mode="wireframe"')
