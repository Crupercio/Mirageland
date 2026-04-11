from django.urls import path

from .views import character_detail

app_name = "catalogue"

urlpatterns = [
    path("characters/<slug:slug>/", character_detail, name="character-detail"),
]
