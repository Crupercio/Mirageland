from __future__ import annotations

from django.db import transaction

from .models import DisplayRoom, OwnedVariant, ShelfSlot

DEFAULT_SLOT_COUNT = 6
ROOM_THEMES = {
    "warm-library": "Warm Library",
    "city-loft": "City Loft",
    "night-studio": "Night Studio",
}


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


def update_room_theme(user, theme_slug: str) -> DisplayRoom:
    if theme_slug not in ROOM_THEMES:
        raise ValueError("Unknown room theme.")

    room = ensure_display_room(user)
    room.theme_slug = theme_slug
    room.save(update_fields=["theme_slug", "updated_at"])
    return room


def toggle_room_reaction(room: DisplayRoom, session: dict) -> bool:
    reacted_room_ids = set(session.get("reacted_room_ids", []))
    room_key = str(room.id)

    if room_key in reacted_room_ids:
        reacted_room_ids.remove(room_key)
        if room.reaction_count > 0:
            room.reaction_count -= 1
        reacted = False
    else:
        reacted_room_ids.add(room_key)
        room.reaction_count += 1
        reacted = True

    room.save(update_fields=["reaction_count", "updated_at"])
    session["reacted_room_ids"] = sorted(reacted_room_ids)
    return reacted
