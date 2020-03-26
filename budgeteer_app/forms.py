from django import forms
from django.forms import ModelForm, Select, TextInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Account, Transaction, TransactionCategory
from functools import partial
from django.forms import modelformset_factory
from django.forms import BaseModelFormSet

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


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
            'account_type': Select(attrs={'style': 'display: block;'}),
        }


class AddTransactionForm(ModelForm):
    # date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}),    label='')

    class Meta(ModelForm):
        model = Transaction
        fields = ['date', 'account', 'amount', 'transaction_type', 'category', 'notes']
        # widgets = {
        #     'account': Select(attrs={'style': 'display: block;'}),
        #     # 'amount': TextInput(attrs={'class': 'col s12 m1'}),
        #     'transaction_type': Select(attrs={'style': 'display: block;'}),
        #     'category': Select(attrs={'style': 'display: block;'}),
        #     # 'notes': TextInput(attrs={'class': 'col s12 m2'}),
        # }
        #
        # labels = {'account': '',
        #          'amount': '',
        #          'transaction_type': '',
        #          'category': '',
        #          'notes': ''}

    def __init__(self, user, *args, **kwargs):
        super(AddTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)
        self.fields['category'].queryset = TransactionCategory.objects.filter(user=user)


# class AddTransactionFormSet(BaseModelFormSet):
#
#     class Meta(BaseModelFormSet):
#         pass
#
#     def __init__(self , user , *args , **kwargs):
#         super().__init__ (*args , **kwargs)
#         self.queryset = Transaction.objects.filter(account__user=user)