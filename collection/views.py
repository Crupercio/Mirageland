from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import DisplayRoom, OwnedVariant
from .services import ROOM_THEMES, ensure_display_room, place_owned_variant, update_room_theme
from .services import toggle_room_reaction


@login_required
@require_GET
def room_detail(request):
    collector = request.user
    room = ensure_display_room(collector)
    room = (
        DisplayRoom.objects.select_related("user")
        .prefetch_related("slots__owned_variant__variant")
        .get(id=room.id)
    )
    owned_variants = (
        OwnedVariant.objects.filter(user=collector)
        .select_related("variant", "variant__character")
        .order_by("variant__unlock_order")
    )

    context = {
        "collector": collector,
        "room": room,
        "owned_variants": owned_variants,
        "room_themes": ROOM_THEMES,
        "current_theme_label": ROOM_THEMES.get(room.theme_slug, "Warm Library"),
        "has_reacted": str(room.id) in request.session.get("reacted_room_ids", []),
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
