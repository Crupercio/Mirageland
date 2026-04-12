from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from catalogue.models import Variant
from collection.models import OwnedVariant

from .models import PlayerQuestStatus, Quest
from .services import bootstrap_player_quests, complete_quest, start_quest


def _build_chapter_sections(player_quests):
    sections = []
    current = None

    for player_quest in player_quests:
        quest = player_quest.quest
        if current is None or current["number"] != quest.chapter_number:
            current = {
                "number": quest.chapter_number,
                "title": quest.chapter_title,
                "player_quests": [],
                "completed_count": 0,
                "total_count": 0,
                "is_active": False,
            }
            sections.append(current)

        current["player_quests"].append(player_quest)
        current["total_count"] += 1
        if player_quest.status == PlayerQuestStatus.COMPLETED:
            current["completed_count"] += 1

    active_chapter_number = None
    for player_quest in player_quests:
        if player_quest.status != PlayerQuestStatus.COMPLETED:
            active_chapter_number = player_quest.quest.chapter_number
            break

    if active_chapter_number is None and sections:
        active_chapter_number = sections[-1]["number"]

    for section in sections:
        section["is_active"] = section["number"] == active_chapter_number

    active_section = next((section for section in sections if section["is_active"]), None)
    return sections, active_section


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
        .order_by("variant__character__name", "variant__unlock_order")
    )
    available_variants = Variant.objects.select_related("character").order_by("unlock_order")
    player_quests = list(player_quests)
    chapter_sections, active_section = _build_chapter_sections(player_quests)

    context = {
        "collector": user,
        "player_quests": player_quests,
        "chapter_sections": chapter_sections,
        "owned_variants": owned_variants,
        "available_variants": available_variants,
        "status_choices": PlayerQuestStatus,
        "chapter_name": active_section["title"] if active_section else "Story Chapter",
        "active_chapter_number": active_section["number"] if active_section else 1,
        "active_chapter_completed_count": active_section["completed_count"] if active_section else 0,
        "active_chapter_total_count": active_section["total_count"] if active_section else 0,
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
