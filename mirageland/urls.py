from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("catalogue/", include("catalogue.urls")),
    path("", include("collection.urls")),
    path("quests/", include("quests.urls")),
    path("admin/", admin.site.urls),
]
