from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import FileResponse, Http404
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
    selected_variant_owned = bool(selected_variant and selected_variant.id in owned_variant_ids)

    context = {
        "collector": collector,
        "character": character,
        "variants": variants,
        "selected_variant": selected_variant,
        "selected_variant_owned": selected_variant_owned,
        "owned_variant_ids": owned_variant_ids,
    }
    return render(request, "catalogue/detail.html", context)


@login_required
def model_asset(request, model_path):
    static_dir = (Path(settings.BASE_DIR) / "static").resolve()
    asset_path = (static_dir / model_path).resolve()

    try:
        asset_path.relative_to(static_dir)
    except ValueError as exc:
        raise Http404("Asset not found.") from exc

    if not asset_path.exists() or asset_path.suffix.lower() != ".glb":
        raise Http404("Asset not found.")

    response = FileResponse(asset_path.open("rb"), content_type="model/gltf-binary")
    response["Content-Disposition"] = f'inline; filename="{asset_path.name}"'
    response["Cache-Control"] = "private, max-age=3600"
    return response
