from django.shortcuts import render


def home(request):
    context = {
        "project_name": "Mirageland",
        "phase_name": "Phase 4: First Playable Progression Loop",
    }
    return render(request, "core/home.html", context)
