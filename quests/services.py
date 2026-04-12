from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from collection.models import OwnedVariant
from collection.services import room_has_any_placement

from .models import PlayerQuest, PlayerQuestStatus, Quest


def bootstrap_player_quests(user) -> list[PlayerQuest]:
    quests = list(Quest.objects.filter(is_active=True).order_by("quest_order"))
    player_quests: list[PlayerQuest] = []

    for index, quest in enumerate(quests):
        player_quest, created = PlayerQuest.objects.get_or_create(
            user=user,
            quest=quest,
            defaults={
                "status": (
                    PlayerQuestStatus.AVAILABLE
                    if index == 0
                    else PlayerQuestStatus.LOCKED
                )
            },
        )
        player_quests.append(player_quest)

        if created:
            continue

        if index == 0 and player_quest.status == PlayerQuestStatus.LOCKED:
            player_quest.status = PlayerQuestStatus.AVAILABLE
            player_quest.save(update_fields=["status", "updated_at"])

    next_unlockable = next(
        (player_quest for player_quest in player_quests if player_quest.status != PlayerQuestStatus.COMPLETED),
        None,
    )
    if next_unlockable and next_unlockable.status == PlayerQuestStatus.LOCKED:
        next_unlockable.status = PlayerQuestStatus.AVAILABLE
        next_unlockable.save(update_fields=["status", "updated_at"])

    return player_quests


@transaction.atomic
def start_quest(user, quest: Quest) -> PlayerQuest:
    bootstrap_player_quests(user)
    player_quest = PlayerQuest.objects.select_for_update().get(user=user, quest=quest)

    if player_quest.status != PlayerQuestStatus.AVAILABLE:
        raise ValueError("Only available quests can be started.")

    player_quest.status = PlayerQuestStatus.ACTIVE
    player_quest.started_at = timezone.now()
    player_quest.save(update_fields=["status", "started_at", "updated_at"])
    return player_quest


@transaction.atomic
def complete_quest(user, quest: Quest) -> PlayerQuest:
    bootstrap_player_quests(user)
    player_quest = PlayerQuest.objects.select_for_update().get(user=user, quest=quest)

    if player_quest.status != PlayerQuestStatus.ACTIVE:
        raise ValueError("Only active quests can be completed.")

    if quest.slug == "shelf-memory" and not room_has_any_placement(user):
        raise ValueError("Place a figurine on the shelf before completing this quest.")

    player_quest.status = PlayerQuestStatus.COMPLETED
    player_quest.completed_at = timezone.now()
    player_quest.save(update_fields=["status", "completed_at", "updated_at"])

    if quest.reward_variant:
        OwnedVariant.objects.get_or_create(user=user, variant=quest.reward_variant)

    if quest.reward_coins:
        user.coins += quest.reward_coins
        user.save(update_fields=["coins"])

    next_player_quest = (
        PlayerQuest.objects.select_for_update()
        .filter(user=user, quest__quest_order__gt=quest.quest_order)
        .order_by("quest__quest_order")
        .first()
    )
    if next_player_quest and next_player_quest.status == PlayerQuestStatus.LOCKED:
        next_player_quest.status = PlayerQuestStatus.AVAILABLE
        next_player_quest.save(update_fields=["status", "updated_at"])

    return player_quest
