from __future__ import annotations

from dataclasses import dataclass
from itertools import groupby

from django.db import transaction

from .models import (
    DisplayRoom,
    OwnedVariant,
    OwnedVariantCustomization,
    OwnedVariantRenderMode,
    ShelfSlot,
)

ROOM_THEMES = {
    "warm-library": "Warm Library",
    "city-loft": "City Loft",
    "night-studio": "Night Studio",
}


@dataclass(frozen=True)
class RoomSlotConfig:
    slot_index: int
    shelf_index: int
    slot_code: str
    display_order: int
    unlock_cost: int
    default_unlocked: bool = False


ROOM_SLOT_LAYOUT: tuple[RoomSlotConfig, ...] = (
    RoomSlotConfig(slot_index=7, shelf_index=1, slot_code="l2", display_order=1, unlock_cost=30),
    RoomSlotConfig(slot_index=1, shelf_index=1, slot_code="l1", display_order=2, unlock_cost=15),
    RoomSlotConfig(slot_index=2, shelf_index=1, slot_code="c", display_order=3, unlock_cost=0, default_unlocked=True),
    RoomSlotConfig(slot_index=3, shelf_index=1, slot_code="r1", display_order=4, unlock_cost=20),
    RoomSlotConfig(slot_index=8, shelf_index=1, slot_code="r2", display_order=5, unlock_cost=40),
    RoomSlotConfig(slot_index=9, shelf_index=2, slot_code="l2", display_order=1, unlock_cost=35),
    RoomSlotConfig(slot_index=4, shelf_index=2, slot_code="l1", display_order=2, unlock_cost=20),
    RoomSlotConfig(slot_index=5, shelf_index=2, slot_code="c", display_order=3, unlock_cost=50),
    RoomSlotConfig(slot_index=6, shelf_index=2, slot_code="r1", display_order=4, unlock_cost=25),
    RoomSlotConfig(slot_index=10, shelf_index=2, slot_code="r2", display_order=5, unlock_cost=45),
)

SLOT_CONFIG_BY_SHELF_AND_CODE = {
    (config.shelf_index, config.slot_code): config for config in ROOM_SLOT_LAYOUT
}


def ensure_display_room(user) -> DisplayRoom:
    room, _ = DisplayRoom.objects.get_or_create(
        user=user,
        defaults={"theme_slug": "warm-library", "is_public": False},
    )

    existing_slots = {
        slot.slot_index: slot
        for slot in room.slots.all()
    }
    new_slots = []

    for config in ROOM_SLOT_LAYOUT:
        slot = existing_slots.get(config.slot_index)
        if slot is None:
            new_slots.append(
                ShelfSlot(
                    room=room,
                    slot_index=config.slot_index,
                    shelf_index=config.shelf_index,
                    slot_code=config.slot_code,
                    display_order=config.display_order,
                    unlock_cost=config.unlock_cost,
                    is_unlocked=config.default_unlocked,
                )
            )
            continue

        dirty_fields = []
        for field_name, expected_value in (
            ("shelf_index", config.shelf_index),
            ("slot_code", config.slot_code),
            ("display_order", config.display_order),
            ("unlock_cost", config.unlock_cost),
        ):
            if getattr(slot, field_name) != expected_value:
                setattr(slot, field_name, expected_value)
                dirty_fields.append(field_name)

        if dirty_fields:
            slot.save(update_fields=dirty_fields)

    if new_slots:
        ShelfSlot.objects.bulk_create(new_slots)

    return room


def get_room_slots(room: DisplayRoom) -> list[ShelfSlot]:
    return list(
        room.slots.select_related(
            "owned_variant",
            "owned_variant__variant",
            "owned_variant__variant__character",
            "owned_variant__customization_state",
        )
        .order_by("shelf_index", "display_order", "slot_index")
    )


def group_slots_by_shelf(slots: list[ShelfSlot]):
    grouped = []
    for shelf_index, grouped_slots in groupby(slots, key=lambda slot: slot.shelf_index):
        shelf_slots = list(grouped_slots)
        grouped.append(
            {
                "shelf_index": shelf_index,
                "label": f"Shelf {shelf_index}",
                "slots": shelf_slots,
                "unlocked_count": sum(1 for slot in shelf_slots if slot.is_unlocked),
                "total_count": len(shelf_slots),
            }
        )
    return grouped


def can_unlock_slot(room: DisplayRoom, slot: ShelfSlot) -> bool:
    if slot.is_unlocked:
        return False

    config = SLOT_CONFIG_BY_SHELF_AND_CODE[(slot.shelf_index, slot.slot_code)]
    shelf_slots = {
        shelf_slot.slot_code: shelf_slot
        for shelf_slot in room.slots.filter(shelf_index=slot.shelf_index)
    }

    if slot.slot_code in {"l1", "r1"}:
        return shelf_slots["c"].is_unlocked

    if slot.slot_code in {"l2", "r2"}:
        return shelf_slots["l1"].is_unlocked and shelf_slots["r1"].is_unlocked

    if slot.slot_code == "c":
        if slot.shelf_index == 1:
            return True

        previous_shelf_slots = room.slots.filter(shelf_index=slot.shelf_index - 1)
        unlocked_previous = {shelf_slot.slot_code for shelf_slot in previous_shelf_slots if shelf_slot.is_unlocked}
        return {"c", "l1", "r1"}.issubset(unlocked_previous)

    return config.default_unlocked


def slot_unlock_label(slot: ShelfSlot) -> str:
    if slot.slot_code == "c" and slot.shelf_index > 1:
        return f"Unlock shelf {slot.shelf_index}"
    return f"Unlock {slot.slot_code.upper()}"


@transaction.atomic
def unlock_room_slot(user, slot_index: int) -> ShelfSlot:
    room = ensure_display_room(user)
    slot = ShelfSlot.objects.select_for_update().get(room=room, slot_index=slot_index)

    if slot.is_unlocked:
        return slot

    if not can_unlock_slot(room, slot):
        raise ValueError("This slot is not available to unlock yet.")

    user = user.__class__.objects.select_for_update().get(pk=user.pk)
    if user.coins < slot.unlock_cost:
        raise ValueError("Not enough coins to unlock this slot.")

    user.coins -= slot.unlock_cost
    user.save(update_fields=["coins"])
    slot.is_unlocked = True
    slot.save(update_fields=["is_unlocked"])
    return slot


@transaction.atomic
def place_owned_variant(user, slot_index: int, owned_variant_id: int | None) -> DisplayRoom:
    room = ensure_display_room(user)
    slot = ShelfSlot.objects.select_for_update().get(room=room, slot_index=slot_index)

    if not slot.is_unlocked:
        raise ValueError("This slot is still locked.")

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


@transaction.atomic
def move_room_slot_variant(user, from_slot_index: int, to_slot_index: int) -> DisplayRoom:
    room = ensure_display_room(user)

    if from_slot_index == to_slot_index:
        return room

    slots = list(
        ShelfSlot.objects.select_for_update()
        .filter(room=room, slot_index__in=[from_slot_index, to_slot_index])
    )
    if len(slots) != 2:
        raise ValueError("Could not find both room slots.")

    slot_map = {slot.slot_index: slot for slot in slots}
    source_slot = slot_map[from_slot_index]
    target_slot = slot_map[to_slot_index]

    if not source_slot.is_unlocked or not target_slot.is_unlocked:
        raise ValueError("Both slots must be unlocked before moving figurines.")

    if source_slot.owned_variant is None:
        raise ValueError("The source slot does not contain a figurine to move.")

    source_variant = source_slot.owned_variant
    target_variant = target_slot.owned_variant

    if target_variant is not None:
        source_slot.owned_variant = None
        source_slot.save(update_fields=["owned_variant"])
        target_slot.owned_variant = source_variant
        target_slot.save(update_fields=["owned_variant"])
        source_slot.owned_variant = target_variant
        source_slot.save(update_fields=["owned_variant"])
        return room

    source_slot.owned_variant = target_variant
    target_slot.owned_variant = source_variant

    source_slot.save(update_fields=["owned_variant"])
    target_slot.save(update_fields=["owned_variant"])
    return room


def room_has_any_placement(user) -> bool:
    return ShelfSlot.objects.filter(
        room__user=user,
        owned_variant__isnull=False,
    ).exists()


def get_or_create_variant_customization(owned_variant: OwnedVariant) -> OwnedVariantCustomization:
    customization_state, _ = OwnedVariantCustomization.objects.get_or_create(
        owned_variant=owned_variant,
        defaults={
            "render_mode": OwnedVariantRenderMode.NORMAL,
            "hidden_parts": [],
            "morph_values": {},
        },
    )
    return customization_state


@transaction.atomic
def update_variant_render_mode(user, owned_variant_id: int, render_mode: str) -> OwnedVariantCustomization:
    return update_variant_customization(
        user,
        owned_variant_id=owned_variant_id,
        render_mode=render_mode,
    )


@transaction.atomic
def update_variant_customization(
    user,
    owned_variant_id: int,
    *,
    render_mode: str | None = None,
    hidden_parts: list[str] | None = None,
    morph_values: dict[str, float] | None = None,
) -> OwnedVariantCustomization:
    if render_mode is not None and render_mode not in OwnedVariantRenderMode.values:
        raise ValueError("Unknown render mode.")

    owned_variant = OwnedVariant.objects.select_for_update().get(
        id=owned_variant_id,
        user=user,
    )
    customization_state = get_or_create_variant_customization(owned_variant)
    update_fields = ["updated_at"]

    if render_mode is not None:
        customization_state.render_mode = render_mode
        update_fields.append("render_mode")

    if hidden_parts is not None:
        cleaned_hidden_parts = sorted(
            {
                str(part_name).strip()
                for part_name in hidden_parts
                if str(part_name).strip()
            }
        )
        customization_state.hidden_parts = cleaned_hidden_parts
        update_fields.append("hidden_parts")

    if morph_values is not None:
        cleaned_morph_values = {}
        for morph_name, morph_value in morph_values.items():
            try:
                cleaned_morph_values[str(morph_name)] = round(float(morph_value), 4)
            except (TypeError, ValueError):
                continue
        customization_state.morph_values = cleaned_morph_values
        update_fields.append("morph_values")

    customization_state.save(update_fields=update_fields)
    return customization_state


@transaction.atomic
def reset_variant_customization(user, owned_variant_id: int) -> OwnedVariantCustomization:
    owned_variant = OwnedVariant.objects.select_for_update().get(
        id=owned_variant_id,
        user=user,
    )
    customization_state = get_or_create_variant_customization(owned_variant)
    customization_state.render_mode = OwnedVariantRenderMode.NORMAL
    customization_state.hidden_parts = []
    customization_state.morph_values = {}
    customization_state.save(update_fields=["render_mode", "hidden_parts", "morph_values", "updated_at"])
    return customization_state


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
