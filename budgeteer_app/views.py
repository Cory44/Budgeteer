from django.shortcuts import render, redirect
from .forms import CustomUserAuthForm, CustomUserCreationForm, AddAccountForm, AddTransactionForm
from django.contrib.auth import logout as lout, login as lin, authenticate
from django.contrib import messages
from .models import Transaction, Account, TransactionCategory
from django.forms import modelformset_factory
# from django.forms import Select


def accounting_num(number):

    if number >= 0:
        str_num = str(number)
        sign = ""
    else:
        str_num = str(number)[1:]
        sign = "-"

    if len(str_num) > 6:
        if len(str_num) > 9:
            acct_num = str_num[:len(str_num)-9] + "," + \
                      str_num[len(str_num)-9:len(str_num)-6] + "," + \
                      str_num[len(str_num)-6:]
            return sign + acct_num
        else:
            acct_num = str_num[:len(str_num)-6] + "," + str_num[len(str_num)-6:]
            return sign + acct_num

    return sign + str_num


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect(f'/{request.user.username}')
    else:
        return render(request, template_name="budgeteer/home.html")


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in!")
        return redirect(f'/{request.user.username}')
    else:
        if request.method == "POST":
            form = CustomUserAuthForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username').lower()
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    lin(request, user)
                    messages.info(request, f"You are now logged in as {user.display_name}")
                    return redirect(f'/{user.username}')
                else:
                    messages.error(request, "Invalid username or password")
            else:
                messages.error(request, "Invalid username or password")

        form = CustomUserAuthForm
        return render(request, "budgeteer/login.html", {"form": form})


def logout(request):
    lout(request)
    return redirect('budgeteer:home')


def register(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are logged in, please log out if you want to register")
        return redirect(f'/{request.user.username}')
    else:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                lin(request, user)
                messages.success(request, f"New account created: {user.display_name}")
                return redirect(f'/{user.username}')
            else:
                for msg in form.errors:
                    for message in form.errors[msg]:
                        messages.error(request, f"{message}")

                return render(request, 'budgeteer/register.html', {"form": form})

        form = CustomUserCreationForm()
        return render(request, 'budgeteer/register.html', {"form": form})


def profile(request, username):

    if username == "admin":
        return redirect('budgeteer:admin')

    if request.user.is_authenticated and request.user.username == username:
        net_worth = 0
        accounts = request.user.account_set.all()
        user_accounts = []

        for account in accounts:
            net_worth += account.current_balance
            user_accounts.append({"name": account.account_name,
                                  "balance": accounting_num(account.current_balance),
                                  "account": account})

        return render(request, "budgeteer/profile/profile.html", {"username": username,
                                                                  "user": request.user,
                                                                  "accounts": user_accounts,
                                                                  "netWorth": accounting_num(net_worth)})
    else:
        return redirect('budgeteer:home')


def add_account(request, username):
    if request.user.is_authenticated and request.user.username == username:
        if request.method == "POST":
            form = AddAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                if len(request.user.account_set.filter(account_name=account.account_name)) > 0:
                    messages.error(request, "Account name already taken")
                    return render(request, 'budgeteer/profile/account/add_account.html', {"form": form})

                account.user = request.user
                form.save()

                messages.success(request, "Account added")
                return render(request, "budgeteer/profile/account/add_account.html", {"form": AddAccountForm()})
            else:
                for msg in form.errors:
                    for message in form.errors[msg]:
                        messages.error(request, f"{message}")

                return render(request, 'budgeteer/profile/account/add_account.html', {"form": form})

        form = AddAccountForm()
        return render(request, "budgeteer/profile/account/add_account.html", {"form": form})
    else:
        return redirect('budgeteer:home')


def add_transaction(request, username, account_name):
    if request.user.is_authenticated and request.user.username == username:

        transaction_formset = modelformset_factory(Transaction, form=AddTransactionForm)

        if request.method == 'POST':

            formset = transaction_formset(request.POST)

            if formset.is_valid():
                transactions = formset.save(commit=False)
                for transaction in transactions:
                    transaction.account = Account.objects.get(account_name=account_name)
                    transaction.save()
                # transactions.save()

                return redirect ('budgeteer:home')

            else:
                print(formset.errors)
                for msg in formset.errors:
                    for item in msg:
                        messages.error(request, f"{msg[item][0]}")

                for msg in formset.non_form_errors():
                    messages.error(request, f"{msg}")

                return render(request, 'budgeteer/profile/add_transaction.html', {"formset": formset})
        else:
            data = {
                'form-TOTAL_FORMS': '10',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': ''}

            formset = transaction_formset(data, queryset=Transaction.objects.filter(account__user=request.user))

            for form in formset:
                form.fields['date'].widget.attrs['class'] = 'datepicker'
                form.fields['category'].queryset = TransactionCategory.objects.filter(user=request.user)

        return render(request, 'budgeteer/profile/add_transaction.html', {"formset": formset})

    else:
        return redirect('budgeteer:home')


def account(request, username, account_name):
    account = request.user.account_set.filter(account_name=account_name)[0]
    transactions = account.transaction_set.all()
    return render(request, "budgeteer/profile/account/account.html", {"account": account,
                                                                      "transactions": transactions,
                                                                      "user": request.user})


def categories(request, username):
    if request.user.is_authenticated and request.user.username == username:
        user = request.user
        categories = TransactionCategory.objects.filter(user=user)
        return render(request, 'budgeteer/profile/categories.html', {"categories": categories})
    else:
        return redirect('budgeteer:home')
