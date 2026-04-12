from django.test import TestCase

from accounts.models import User
from catalogue.models import Character, Variant, VariantRarity, VariantSceneType
from collection.models import OwnedVariant
from collection.services import place_owned_variant

from .models import PlayerQuest, PlayerQuestStatus, Quest
from .services import bootstrap_player_quests, complete_quest, start_quest


class QuestProgressionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="collector", password="testpass123")
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
        self.quest_one = Quest.objects.create(
            slug="first-light",
            title="First Light",
            description="Meet Sora and receive her base figurine.",
            chapter_number=1,
            chapter_title="Chapter 1 - First Light",
            quest_order=1,
            reward_variant=self.base_variant,
        )
        self.quest_two = Quest.objects.create(
            slug="margin-notes",
            title="Margin Notes",
            description="Revisit Sora and receive the school variant.",
            chapter_number=1,
            chapter_title="Chapter 1 - First Light",
            quest_order=2,
            reward_variant=self.school_variant,
            reward_coins=15,
        )
        self.quest_three = Quest.objects.create(
            slug="shelf-memory",
            title="Shelf Memory",
            description="Place Sora onto the shelf.",
            chapter_number=1,
            chapter_title="Chapter 1 - First Light",
            quest_order=3,
            reward_coins=25,
        )

    def test_bootstrap_creates_first_available_and_rest_locked(self):
        player_quests = bootstrap_player_quests(self.user)

        self.assertEqual(len(player_quests), 3)
        self.assertEqual(player_quests[0].status, PlayerQuestStatus.AVAILABLE)
        self.assertEqual(player_quests[1].status, PlayerQuestStatus.LOCKED)
        self.assertEqual(player_quests[2].status, PlayerQuestStatus.LOCKED)

    def test_complete_quest_awards_rewards_and_unlocks_next(self):
        bootstrap_player_quests(self.user)
        start_quest(self.user, self.quest_one)
        complete_quest(self.user, self.quest_one)

        self.assertTrue(
            OwnedVariant.objects.filter(user=self.user, variant=self.base_variant).exists()
        )
        next_state = PlayerQuest.objects.get(user=self.user, quest=self.quest_two)
        self.assertEqual(next_state.status, PlayerQuestStatus.AVAILABLE)

        start_quest(self.user, self.quest_two)
        complete_quest(self.user, self.quest_two)

        self.user.refresh_from_db()
        self.assertEqual(self.user.coins, 15)
        self.assertTrue(
            OwnedVariant.objects.filter(user=self.user, variant=self.school_variant).exists()
        )

    def test_cannot_complete_quest_before_starting(self):
        bootstrap_player_quests(self.user)

        with self.assertRaises(ValueError):
            complete_quest(self.user, self.quest_one)

    def test_shelf_memory_requires_actual_room_placement(self):
        bootstrap_player_quests(self.user)
        start_quest(self.user, self.quest_one)
        complete_quest(self.user, self.quest_one)
        start_quest(self.user, self.quest_two)
        complete_quest(self.user, self.quest_two)
        start_quest(self.user, self.quest_three)

        with self.assertRaises(ValueError):
            complete_quest(self.user, self.quest_three)

        owned_variant = OwnedVariant.objects.get(user=self.user, variant=self.base_variant)
        place_owned_variant(self.user, slot_index=1, owned_variant_id=owned_variant.id)
        complete_quest(self.user, self.quest_three)

        self.user.refresh_from_db()
        self.assertEqual(self.user.coins, 40)

    def test_bootstrap_handles_multiple_chapters_in_global_order(self):
        ren_character = Character.objects.create(
            name="Ren Takahashi",
            archetype="The Rival / Hidden Heart",
            short_description="A watchful protector at the edge of the frame.",
            lore_quote="Staying doesn't have to look soft to still count.",
            color_hex="#445C8C",
        )
        ren_variant = Variant.objects.create(
            character=ren_character,
            name="Ren Base",
            scene_type=VariantSceneType.BASE,
            unlock_order=4,
            rarity=VariantRarity.STANDARD,
            short_description="Ren at a city corner.",
            model_file_path="models/characters/ren/base.glb",
        )
        chapter_two_quest = Quest.objects.create(
            slug="street-corner-promise",
            title="Street Corner Promise",
            description="Meet Ren after Sora's opening chapter.",
            chapter_number=2,
            chapter_title="Chapter 2 - Sharp Edges",
            quest_order=4,
            reward_variant=ren_variant,
            reward_coins=10,
        )

        bootstrap_player_quests(self.user)
        start_quest(self.user, self.quest_one)
        complete_quest(self.user, self.quest_one)
        start_quest(self.user, self.quest_two)
        complete_quest(self.user, self.quest_two)
        start_quest(self.user, self.quest_three)

        owned_variant = OwnedVariant.objects.get(user=self.user, variant=self.base_variant)
        place_owned_variant(self.user, slot_index=1, owned_variant_id=owned_variant.id)
        complete_quest(self.user, self.quest_three)

        chapter_two_state = PlayerQuest.objects.get(user=self.user, quest=chapter_two_quest)
        self.assertEqual(chapter_two_state.status, PlayerQuestStatus.AVAILABLE)
