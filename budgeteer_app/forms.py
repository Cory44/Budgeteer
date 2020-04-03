# from django import forms
from django.forms import ModelForm, Select, DateField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Account, Transaction, TransactionCategory
from django import forms
from budgeteer.settings import DATE_INPUT_FORMATS


# Form to log a user into thier acount
class CustomUserAuthForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        model = User
        fields = ('username', 'password')

    def clean_username(self):
        return self.cleaned_data['username'].lower()


# Form to create a new User
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'password1', 'password2']


# Form to add an account
class AddAccountForm(ModelForm):
    class Meta(ModelForm):
        model = Account
        fields = ['account_name', 'account_type', 'starting_balance']
        widgets = {
            'account_type': Select(attrs={'style': 'display: block;'}),
        }

class AddTransactionForm(ModelForm):
    date = forms.DateField(input_formats=DATE_INPUT_FORMATS,)
    class Meta:
        model = Transaction
        fields = ('date', 'amount', 'transaction_type', 'category', 'notes')
        widgets = {'transaction_type': Select(attrs={'style': 'display: block;'}),
                   'category': Select(attrs={'style': 'display: block;'}),
                   # 'date': DateField(input_formats=)
                   }


class AddExpenseCategory(ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ('category',)

