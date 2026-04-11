from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    context = {
        "project_name": "Mirageland",
        "phase_name": "Authentication And Real Player Accounts",
    }
    return render(request, "core/home.html", context)


def healthcheck(request):
    return JsonResponse({"status": "ok"})
