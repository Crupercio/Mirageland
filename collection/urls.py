from django.urls import path

from .views import (
    room_detail,
    room_move_variant,
    room_place_variant,
    room_toggle_reaction,
    room_toggle_visibility,
    room_unlock_slot,
    room_update_theme,
)

app_name = "collection"

urlpatterns = [
    path("room/", room_detail, name="room-detail"),
    path("room/slots/move/", room_move_variant, name="room-move-variant"),
    path("room/slots/<int:slot_index>/place/", room_place_variant, name="room-place-variant"),
    path("room/slots/<int:slot_index>/unlock/", room_unlock_slot, name="room-unlock-slot"),
    path("room/visibility/", room_toggle_visibility, name="room-toggle-visibility"),
    path("room/theme/", room_update_theme, name="room-update-theme"),
    path("room/react/", room_toggle_reaction, name="room-toggle-reaction"),
]
