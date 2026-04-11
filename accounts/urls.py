from django.urls import path

from .views import MiragelandLoginView, MiragelandLogoutView, account_view, signup_view

app_name = "accounts"

urlpatterns = [
    path("login/", MiragelandLoginView.as_view(), name="login"),
    path("logout/", MiragelandLogoutView.as_view(), name="logout"),
    path("signup/", signup_view, name="signup"),
    path("me/", account_view, name="account"),
]
