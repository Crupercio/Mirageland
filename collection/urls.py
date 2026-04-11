from django.urls import path

from .views import room_detail, room_place_variant, room_toggle_visibility

app_name = "collection"

urlpatterns = [
    path("room/", room_detail, name="room-detail"),
    path("room/slots/<int:slot_index>/place/", room_place_variant, name="room-place-variant"),
    path("room/visibility/", room_toggle_visibility, name="room-toggle-visibility"),
]
