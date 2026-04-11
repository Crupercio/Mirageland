from django.shortcuts import get_object_or_404, render

from collection.models import OwnedVariant
from core.demo import get_demo_user

from .models import Character


def character_detail(request, slug):
    collector = request.user if request.user.is_authenticated else get_demo_user()
    character = get_object_or_404(
        Character.objects.prefetch_related("variants").all(),
        slug=slug,
    )
    variants = list(character.variants.order_by("unlock_order"))
    selected_slug = request.GET.get("variant")
    selected_variant = next(
        (variant for variant in variants if variant.slug == selected_slug),
        variants[0] if variants else None,
    )

    owned_variant_ids = set(
        OwnedVariant.objects.filter(user=collector, variant__character=character)
        .values_list("variant_id", flat=True)
    )

    context = {
        "collector": collector,
        "character": character,
        "variants": variants,
        "selected_variant": selected_variant,
        "owned_variant_ids": owned_variant_ids,
    }
    return render(request, "catalogue/detail.html", context)
