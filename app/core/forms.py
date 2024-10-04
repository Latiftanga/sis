from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm, UserCreationForm
)
from django.contrib.auth import get_user_model
from core import models


class UserRegistrationForm(UserCreationForm):
    """User registration form"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        # Retrieve initial email from kwargs
        initial_email = kwargs.pop('initial_email', None)
        super().__init__(*args, **kwargs)
        if initial_email:
            self.fields['email'].initial = initial_email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch.")

        return cleaned_data


class TokenVerificationForm(forms.Form):
    token = forms.CharField(help_text="Enter the token provided by the admin.")

    def clean_token(self):
        token = self.cleaned_data.get('token')
        if not models.SignupToken.objects.filter(token=token, is_used=False).exists():
            raise forms.ValidationError("Invalid or already used token.")
        return token


class SigninForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            }
        ), label='Password'
        )


class ChangePasswordForm(PasswordChangeForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "old password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "new password",
                "class": "form-control"
            }
        ))

    class Meta:
        model = get_user_model()
        fields = ('password1', 'password2')


class AddressForm(forms.ModelForm):
    """Form for Address"""
    class Meta:
        model = models.Address
        fields = '__all__'
