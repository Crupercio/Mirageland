from django.urls import path

from .views import quest_complete, quest_hub, quest_start

app_name = "quests"

urlpatterns = [
    path("", quest_hub, name="hub"),
    path("<slug:slug>/start/", quest_start, name="start"),
    path("<slug:slug>/complete/", quest_complete, name="complete"),
]

