from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from catalogue.models import Variant
from collection.models import OwnedVariant

from .models import PlayerQuestStatus, Quest
from .services import bootstrap_player_quests, complete_quest, start_quest


@login_required
@require_GET
def quest_hub(request: HttpRequest):
    user = request.user
    bootstrap_player_quests(user)

    player_quests = (
        user.player_quests.select_related("quest", "quest__reward_variant")
        .order_by("quest__quest_order")
    )
    owned_variants = (
        OwnedVariant.objects.filter(user=user)
        .select_related("variant", "variant__character")
        .order_by("variant__unlock_order")
    )
    available_variants = Variant.objects.select_related("character").order_by("unlock_order")

    context = {
        "collector": user,
        "player_quests": player_quests,
        "owned_variants": owned_variants,
        "available_variants": available_variants,
        "status_choices": PlayerQuestStatus,
        "chapter_name": "Chapter 1 - First Light",
        "completed_count": sum(
            1 for player_quest in player_quests if player_quest.status == PlayerQuestStatus.COMPLETED
        ),
        "total_count": len(player_quests),
    }
    return render(request, "quests/hub.html", context)


@login_required
@require_POST
def quest_start(request: HttpRequest, slug: str):
    user = request.user
    quest = get_object_or_404(Quest, slug=slug, is_active=True)

    try:
        start_quest(user, quest)
    except ValueError:
        return HttpResponseBadRequest("Quest cannot be started right now.")

    return redirect("quests:hub")


@login_required
@require_POST
def quest_complete(request: HttpRequest, slug: str):
    user = request.user
    quest = get_object_or_404(Quest, slug=slug, is_active=True)

    try:
        complete_quest(user, quest)
    except ValueError:
        return HttpResponseBadRequest("Quest cannot be completed right now.")

    return redirect("quests:hub")
