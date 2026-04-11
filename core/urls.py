from django.urls import path

from .views import healthcheck, home

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("health/", healthcheck, name="health"),
]
