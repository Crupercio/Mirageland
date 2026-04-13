from django.urls import path

from .views import (
    catalogue_index,
    character_detail,
    customization_lab,
    model_asset,
    reset_variant_display_state,
    save_variant_render_mode,
    viewer_plate_asset,
)

app_name = "catalogue"

urlpatterns = [
    path("", catalogue_index, name="index"),
    path("lab/", customization_lab, name="lab"),
    path("model-assets/<path:model_path>", model_asset, name="model-asset"),
    path("viewer-plates/<str:plate_name>", viewer_plate_asset, name="viewer-plate"),
    path("owned-variants/render-mode/", save_variant_render_mode, name="save-render-mode"),
    path("owned-variants/reset-state/", reset_variant_display_state, name="reset-display-state"),
    path("characters/<slug:slug>/", character_detail, name="character-detail"),
]
