from django.urls import path

from .views import catalogue_index, character_detail, model_asset

app_name = "catalogue"

urlpatterns = [
    path("", catalogue_index, name="index"),
    path("model-assets/<path:model_path>", model_asset, name="model-asset"),
    path("characters/<slug:slug>/", character_detail, name="character-detail"),
]
