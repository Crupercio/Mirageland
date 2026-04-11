from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from core.demo import get_demo_user

from .models import DisplayRoom, OwnedVariant
from .services import ensure_display_room, place_owned_variant


@require_GET
def room_detail(request):
    collector = request.user if request.user.is_authenticated else get_demo_user()
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
    }
    return render(request, "collection/room.html", context)


@require_POST
def room_place_variant(request, slot_index: int):
    collector = request.user if request.user.is_authenticated else get_demo_user()
    owned_variant_id = request.POST.get("owned_variant_id")

    try:
        parsed_id = int(owned_variant_id) if owned_variant_id else None
        place_owned_variant(collector, slot_index=slot_index, owned_variant_id=parsed_id)
    except (ValueError, OwnedVariant.DoesNotExist):
        return HttpResponseBadRequest("Could not place that variant in the selected slot.")

    return redirect("collection:room-detail")


@require_POST
def room_toggle_visibility(request):
    collector = request.user if request.user.is_authenticated else get_demo_user()
    room = ensure_display_room(collector)
    room.is_public = request.POST.get("is_public") == "true"
    room.save(update_fields=["is_public"])
    return redirect("collection:room-detail")
