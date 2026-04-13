from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import DisplayRoom, OwnedVariant
from .services import (
    ROOM_THEMES,
    can_unlock_slot,
    ensure_display_room,
    get_room_slots,
    move_room_slot_variant,
    group_slots_by_shelf,
    place_owned_variant,
    slot_unlock_label,
    toggle_room_reaction,
    unlock_room_slot,
    update_room_theme,
)


@login_required
@require_GET
def room_detail(request):
    collector = request.user
    room = ensure_display_room(collector)
    room = (
        DisplayRoom.objects.select_related("user")
        .prefetch_related("slots__owned_variant__variant__character")
        .get(id=room.id)
    )
    room_slots = get_room_slots(room)
    for slot in room_slots:
        slot.can_unlock = can_unlock_slot(room, slot)
        slot.unlock_label = slot_unlock_label(slot)
        slot.coins_short = max(slot.unlock_cost - collector.coins, 0)

    owned_variants = (
        OwnedVariant.objects.filter(user=collector)
        .select_related("variant", "variant__character")
        .order_by("variant__unlock_order")
    )

    context = {
        "collector": collector,
        "room": room,
        "room_slots": room_slots,
        "room_shelves": group_slots_by_shelf(room_slots),
        "owned_variants": owned_variants,
        "room_themes": ROOM_THEMES,
        "current_theme_label": ROOM_THEMES.get(room.theme_slug, "Warm Library"),
        "has_reacted": str(room.id) in request.session.get("reacted_room_ids", []),
        "unlocked_slot_count": sum(1 for slot in room_slots if slot.is_unlocked),
    }
    return render(request, "collection/room.html", context)


@login_required
@require_POST
def room_place_variant(request, slot_index: int):
    collector = request.user
    owned_variant_id = request.POST.get("owned_variant_id")

    try:
        parsed_id = int(owned_variant_id) if owned_variant_id else None
        place_owned_variant(collector, slot_index=slot_index, owned_variant_id=parsed_id)
    except (ValueError, OwnedVariant.DoesNotExist):
        return HttpResponseBadRequest("Could not place that variant in the selected slot.")

    return redirect("collection:room-detail")


@login_required
@require_POST
def room_unlock_slot(request, slot_index: int):
    collector = request.user

    try:
        unlock_room_slot(collector, slot_index=slot_index)
    except ValueError as exc:
        return HttpResponseBadRequest(str(exc))

    return redirect("collection:room-detail")


@login_required
@require_POST
def room_move_variant(request):
    collector = request.user

    try:
        from_slot_index = int(request.POST.get("from_slot_index", ""))
        to_slot_index = int(request.POST.get("to_slot_index", ""))
        move_room_slot_variant(collector, from_slot_index=from_slot_index, to_slot_index=to_slot_index)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Could not move that figurine between shelf slots.")

    return redirect("collection:room-detail")


@login_required
@require_POST
def room_toggle_visibility(request):
    collector = request.user
    room = ensure_display_room(collector)
    room.is_public = request.POST.get("is_public") == "true"
    room.save(update_fields=["is_public"])
    return redirect("collection:room-detail")


@login_required
@require_POST
def room_update_theme(request):
    collector = request.user
    theme_slug = request.POST.get("theme_slug", "")

    try:
        update_room_theme(collector, theme_slug)
    except ValueError:
        return HttpResponseBadRequest("Unknown room theme selection.")

    return redirect("collection:room-detail")


@login_required
@require_POST
def room_toggle_reaction(request):
    collector = request.user
    room = ensure_display_room(collector)

    if not room.is_public:
        return HttpResponseBadRequest("Room must be public before it can receive reactions.")

    if request.session.session_key is None:
        request.session.save()

    toggle_room_reaction(room, request.session)
    request.session.modified = True
    return redirect("collection:room-detail")
