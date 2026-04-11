from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import MiragelandLoginForm, MiragelandSignupForm


class MiragelandLoginView(LoginView):
    authentication_form = MiragelandLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class MiragelandLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    form = MiragelandSignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("catalogue:index")

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def account_view(request):
    context = {
        "collector": request.user,
    }
    return render(request, "accounts/account.html", context)
