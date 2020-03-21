from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

# Form to create a user
class CustomUserAuthForm(AuthenticationForm):
    # username = UserNameField(max_length=50)

    class meta(AuthenticationForm):
        model = User
        fields = ('username', 'password')

    def clean_username(self):
        return self.cleaned_data['username'].lower()
