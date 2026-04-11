from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from collection.models import OwnedVariant

from .models import Character


@login_required
def catalogue_index(request):
    collector = request.user
    characters = (
        Character.objects.annotate(
            total_variants=Count("variants", distinct=True),
            owned_variants=Count(
                "variants__owners",
                filter=Q(variants__owners__user=collector),
                distinct=True,
            ),
        )
        .order_by("name")
    )

    context = {
        "collector": collector,
        "characters": characters,
    }
    return render(request, "catalogue/index.html", context)


@login_required
def character_detail(request, slug):
    collector = request.user
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
