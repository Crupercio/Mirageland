from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class MiragelandSignupForm(UserCreationForm):
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Choose a collector name", "autocomplete": "username"}
        )
        self.fields["email"].widget.attrs.update(
            {"placeholder": "Optional email for later", "autocomplete": "email"}
        )
        self.fields["password1"].widget.attrs.update({"autocomplete": "new-password"})
        self.fields["password2"].widget.attrs.update({"autocomplete": "new-password"})
        self.fields["email"].help_text = "Optional. You can leave this blank for testing."

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class MiragelandLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Your collector username", "autocomplete": "username"}
        )
        self.fields["password"].widget.attrs.update({"autocomplete": "current-password"})
