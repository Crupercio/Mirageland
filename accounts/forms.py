from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class MiragelandSignupForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class MiragelandLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
