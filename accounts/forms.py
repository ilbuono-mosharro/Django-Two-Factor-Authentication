from typing import Any
from django import forms
from .models import TwoFactorAuth
from django.contrib.auth.forms import AuthenticationForm, UsernameField

class TwoFactorForm(forms.ModelForm):
    class Meta:
        model = TwoFactorAuth
        fields = ("code",)
        widgets = {
            'code': forms.TextInput(attrs={"class": "form-control mb-4"})
        }

class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.EmailInput(attrs={"autofocus": True}))

    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})
