from django.shortcuts import render


def home(request):
    context = {
        "project_name": "Mirageland",
        "phase_name": "Phase 2: Local Dev Foundation",
    }
    return render(request, "core/home.html", context)
