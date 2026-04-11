from __future__ import annotations

from django.db import transaction

from .models import DisplayRoom, OwnedVariant, ShelfSlot

DEFAULT_SLOT_COUNT = 6


def ensure_display_room(user, slot_count: int = DEFAULT_SLOT_COUNT) -> DisplayRoom:
    room, _ = DisplayRoom.objects.get_or_create(
        user=user,
        defaults={"theme_slug": "warm-library", "is_public": False},
    )

    existing_slots = set(room.slots.values_list("slot_index", flat=True))
    missing_slots = [
        ShelfSlot(room=room, slot_index=index)
        for index in range(1, slot_count + 1)
        if index not in existing_slots
    ]
    if missing_slots:
        ShelfSlot.objects.bulk_create(missing_slots)

    return room


@transaction.atomic
def place_owned_variant(user, slot_index: int, owned_variant_id: int | None) -> DisplayRoom:
    room = ensure_display_room(user)
    slot = ShelfSlot.objects.select_for_update().get(room=room, slot_index=slot_index)

    if not owned_variant_id:
        slot.owned_variant = None
        slot.save(update_fields=["owned_variant"])
        return room

    owned_variant = OwnedVariant.objects.select_for_update().get(
        id=owned_variant_id,
        user=user,
    )

    previous_slot = (
        ShelfSlot.objects.select_for_update()
        .filter(owned_variant=owned_variant)
        .exclude(id=slot.id)
        .first()
    )
    if previous_slot:
        previous_slot.owned_variant = None
        previous_slot.save(update_fields=["owned_variant"])

    slot.owned_variant = owned_variant
    slot.save(update_fields=["owned_variant"])
    return room


def room_has_any_placement(user) -> bool:
    return ShelfSlot.objects.filter(
        room__user=user,
        owned_variant__isnull=False,
    ).exists()
