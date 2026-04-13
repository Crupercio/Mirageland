import json
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from collection.models import OwnedVariant, OwnedVariantRenderMode
from collection.services import (
    filter_hideable_parts,
    reset_all_variant_customizations,
    reset_variant_customization,
    update_variant_customization,
)

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

    owned_variants = list(
        OwnedVariant.objects.filter(user=collector, variant__character=character)
        .select_related("variant", "customization_state")
    )
    owned_variant_ids = {owned_variant.variant_id for owned_variant in owned_variants}
    selected_variant_owned = bool(selected_variant and selected_variant.id in owned_variant_ids)
    selected_owned_variant = next(
        (owned_variant for owned_variant in owned_variants if selected_variant and owned_variant.variant_id == selected_variant.id),
        None,
    )
    selected_customization = getattr(selected_owned_variant, "customization_state", None)

    context = {
        "collector": collector,
        "character": character,
        "variants": variants,
        "selected_variant": selected_variant,
        "selected_variant_owned": selected_variant_owned,
        "selected_owned_variant": selected_owned_variant,
        "selected_render_mode": (
            selected_customization.render_mode
            if selected_customization
            else OwnedVariantRenderMode.NORMAL
        ),
        "selected_hidden_parts_json": json.dumps(
            filter_hideable_parts(selected_customization.hidden_parts)
            if selected_customization
            else []
        ),
        "selected_morph_values_json": json.dumps(
            selected_customization.morph_values if selected_customization else {}
        ),
        "owned_variant_ids": owned_variant_ids,
    }
    return render(request, "catalogue/detail.html", context)


@login_required
def customization_lab(request):
    collector = request.user
    owned_variants = list(
        OwnedVariant.objects.filter(user=collector)
        .select_related("variant", "variant__character", "customization_state")
        .order_by("variant__character__name", "variant__unlock_order", "id")
    )

    selected_owned_variant = None
    selected_owned_variant_id = request.GET.get("owned_variant")
    if selected_owned_variant_id:
        try:
            selected_owned_variant = next(
                owned_variant
                for owned_variant in owned_variants
                if owned_variant.id == int(selected_owned_variant_id)
            )
        except (StopIteration, ValueError):
            selected_owned_variant = None

    if selected_owned_variant is None and owned_variants:
        selected_owned_variant = owned_variants[0]

    selected_character = selected_owned_variant.variant.character if selected_owned_variant else None
    selected_variant = selected_owned_variant.variant if selected_owned_variant else None
    selected_customization = (
        getattr(selected_owned_variant, "customization_state", None)
        if selected_owned_variant
        else None
    )

    context = {
        "collector": collector,
        "owned_variants": owned_variants,
        "selected_owned_variant": selected_owned_variant,
        "selected_character": selected_character,
        "selected_variant": selected_variant,
        "selected_render_mode": (
            selected_customization.render_mode
            if selected_customization
            else OwnedVariantRenderMode.NORMAL
        ),
        "selected_hidden_parts_json": json.dumps(
            filter_hideable_parts(selected_customization.hidden_parts)
            if selected_customization
            else []
        ),
        "selected_morph_values_json": json.dumps(
            selected_customization.morph_values if selected_customization else {}
        ),
    }
    return render(request, "catalogue/lab.html", context)


@login_required
@require_POST
def save_variant_render_mode(request):
    owned_variant_id = request.POST.get("owned_variant_id")
    render_mode = request.POST.get("render_mode", "")
    hidden_parts_raw = request.POST.get("hidden_parts", "")
    morph_values_raw = request.POST.get("morph_values", "")

    hidden_parts = None
    morph_values = None
    if hidden_parts_raw:
        try:
            hidden_parts = json.loads(hidden_parts_raw)
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Hidden parts payload is invalid."}, status=400)
    if morph_values_raw:
        try:
            morph_values = json.loads(morph_values_raw)
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Morph values payload is invalid."}, status=400)

    try:
        customization_state = update_variant_customization(
            request.user,
            owned_variant_id=int(owned_variant_id or ""),
            render_mode=render_mode,
            hidden_parts=hidden_parts,
            morph_values=morph_values,
        )
    except (TypeError, ValueError, OwnedVariant.DoesNotExist):
        return JsonResponse({"ok": False, "error": "Could not save the customization state."}, status=400)

    return JsonResponse(
        {
            "ok": True,
            "render_mode": customization_state.render_mode,
            "hidden_parts": customization_state.hidden_parts,
            "morph_values": customization_state.morph_values,
        }
    )


@login_required
@require_POST
def reset_variant_display_state(request):
    owned_variant_id = request.POST.get("owned_variant_id")
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/catalogue/"

    try:
        customization_state = reset_variant_customization(
            request.user,
            owned_variant_id=int(owned_variant_id or ""),
        )
    except (TypeError, ValueError, OwnedVariant.DoesNotExist):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {"ok": False, "error": "Could not reset the customization state."},
                status=400,
            )
        return redirect(next_url)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "ok": True,
                "render_mode": customization_state.render_mode,
                "hidden_parts": customization_state.hidden_parts,
                "morph_values": customization_state.morph_values,
            }
        )

    return redirect(next_url)


@login_required
@require_POST
def reset_all_variant_display_states(request):
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/catalogue/lab/"
    reset_count = reset_all_variant_customizations(request.user)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "reset_count": reset_count})

    return redirect(next_url)


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


@login_required
def viewer_plate_asset(request, plate_name):
    plates_dir = (Path(settings.BASE_DIR) / "static" / "images" / "viewer-plates").resolve()
    asset_path = (plates_dir / plate_name).resolve()

    try:
        asset_path.relative_to(plates_dir)
    except ValueError as exc:
        raise Http404("Plate not found.") from exc

    if not asset_path.exists() or asset_path.suffix.lower() not in {".svg", ".png", ".jpg", ".jpeg", ".webp"}:
        raise Http404("Plate not found.")

    content_type = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }[asset_path.suffix.lower()]
    response = FileResponse(asset_path.open("rb"), content_type=content_type)
    response["Content-Disposition"] = f'inline; filename="{asset_path.name}"'
    response["Cache-Control"] = "private, max-age=3600"
    return response
