# from django import forms
# from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


# Form to create a user
class CustomUserAuthForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        model = User
        fields = ('username', 'password')

    def clean_username(self):
        return self.cleaned_data['username'].lower()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'password1', 'password2']
