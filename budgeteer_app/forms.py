from django import forms
from django.forms import ModelForm, Select
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Account, AccountType


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

class AddAccountForm(ModelForm):
    # starting_balance = forms.DecimalField(max_digits=12, decimal_places=2)

    class Meta(ModelForm):
        model = Account
        fields = ['account_name', 'account_type', 'starting_balance']
        widgets = {
            'account_type': Select(attrs={'style': 'display: block;'}) ,
        }

# class AddAccountForm(forms.Form):
#     account_name = forms.CharField(max_length=100)
#     account_type = forms.ModelChoiceField(queryset=AccountType.objects.all(), empty_label=None)
#     starting_balance = forms.DecimalField(max_digits=12, decimal_places=2)
#
#
