from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    context = {
        "project_name": "Mirageland",
        "phase_name": "UI Polish And Player Experience Pass",
    }
    return render(request, "core/home.html", context)


def healthcheck(request):
    return JsonResponse({"status": "ok"})
