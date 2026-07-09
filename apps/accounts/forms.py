


from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .validators import (
    validate_name,
    validate_username,
)

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
    Form used for customer registration.
    """

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8,
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8,
        label="Confirm Password",
    )

    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]

        validate_username(username)

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username is already taken."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email is already registered."
            )

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]

        validate_name(first_name)

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]

        validate_name(last_name)

        return last_name

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data


class LoginForm(forms.Form):
    """
    User login form.
    """

    username = forms.CharField(max_length=150)

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:

            user = authenticate(
                username=username,
                password=password,
            )

            if user is None:
                raise forms.ValidationError(
                    "Invalid username or password."
                )

            cleaned_data["user"] = user

        return cleaned_data