from django.urls import path

from .views import catalogue_index, character_detail

app_name = "catalogue"

urlpatterns = [
    path("", catalogue_index, name="index"),
    path("characters/<slug:slug>/", character_detail, name="character-detail"),
]
