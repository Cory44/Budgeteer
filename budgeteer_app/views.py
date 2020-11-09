from django.shortcuts import render, redirect
from .forms import CustomUserAuthForm, CustomUserCreationForm, AddAccountForm, AddTransactionForm, AddExpenseCategory
from django.contrib.auth import logout as lout
from django.contrib import messages
from .models import Transaction, TransactionCategory, TransactionType, Account, Budget
from django.forms import modelformset_factory
from .view_helpers.add_transaction import get_categories, validate_transaction_formset, clean_formset
from .view_helpers.general import accounting_num
from .view_helpers.delete_transaction import delete_offset
from .view_helpers.graphing import graph
from .view_helpers.categories import create_category
from .view_helpers.add_account import validate_account_form
from .view_helpers.register import validate_registration
from .view_helpers.login import validate_login
from .view_helpers.edit import update_user
from django.db.models import Sum


def home(request):
    if request.user.is_authenticated:
        return redirect("budgeteer:profile", request.user.username)
    else:
        return render(request, template_name="budgeteer/home.html")


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in!")
        return redirect(f'/{request.user.username}')
    else:
        if request.method == "POST":
            form = CustomUserAuthForm(request, data=request.POST)
            return validate_login(request, form)

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
            return validate_registration(request, form)

        form = CustomUserCreationForm()
        return render(request, 'budgeteer/register.html', {"form": form})


def profile(request, username):

    if username == "admin":
        return redirect('budgeteer:admin')

    if request.user.is_authenticated and request.user.username == username:
        net_worth = 0
        accounts = request.user.account_set.all()
        user_accounts = []

        for each_account in accounts:
            net_worth += each_account.current_balance
            user_accounts.append({"name": each_account.account_name,
                                  "balance": accounting_num(each_account.current_balance),
                                  "account": each_account})

        return render(request, "budgeteer/profile/profile.html", {"accounts": user_accounts,
                                                                  "netWorth": accounting_num(net_worth), })
    else:
        return redirect('budgeteer:home')


def add_account(request, username):
    if request.user.is_authenticated and request.user.username == username:
        if request.method == "POST":
            form = AddAccountForm(request.POST)
            return validate_account_form(request, form)

        form = AddAccountForm()
        return render(request, "budgeteer/profile/account/add_account.html", {"form": form})
    else:
        return redirect('budgeteer:home')


def add_transaction(request, username, account_name):
    if request.user.is_authenticated and request.user.username == username:
        transaction_formset = modelformset_factory(Transaction, form=AddTransactionForm)
        expense_categories, income_categories, transfer_categories, value_adjust_categories = get_categories(request)
        context = {"formset": transaction_formset, "expense_categories": expense_categories,
                   "income_categories": income_categories, "transfer_categories": transfer_categories,
                   "value_adjust_categories": value_adjust_categories}

        if request.method == 'POST':
            formset = transaction_formset(request.POST)
            cleaned_formset = clean_formset(request, formset)
            context['formset'] = cleaned_formset

            return validate_transaction_formset(request, cleaned_formset, account_name, context)

        else:
            data = {'form-TOTAL_FORMS': '10',
                    'form-INITIAL_FORMS': '0',
                    'form-MAX_NUM_FORMS': ''}

            formset = transaction_formset(data, queryset=Transaction.objects.filter(account__user=request.user))
            context['formset'] = formset

            for form in formset:
                form.fields['date'].widget.attrs['class'] = 'datepicker'

        return render(request, 'budgeteer/profile/add_transaction.html', context)

    else:
        return redirect('budgeteer:home')


def account(request, username, account_name):
    display_account = request.user.account_set.filter(account_name=account_name)[0]
    transactions = display_account.transaction_set.all()
    return render(request, 'budgeteer/profile/account/account.html', {"account": display_account,
                                                                      "transactions": transactions,
                                                                      "username": username})


def categories(request, username):
    if request.user.is_authenticated and request.user.username == username:

        user = request.user
        expense = TransactionType.objects.get(type_name="Expense")
        income = TransactionType.objects.get(type_name="Income")
        transfer = TransactionType.objects.get(type_name="Transfer")

        expense_categories = TransactionCategory.objects.filter(user=user, transaction_type=expense)
        income_categories = TransactionCategory.objects.filter(user=user, transaction_type=income)
        transfer_categories = TransactionCategory.objects.filter(user=user, transaction_type=transfer)

        expense_category_form = AddExpenseCategory(prefix="expense_category")
        income_category_form = AddExpenseCategory(prefix="income_category")

        context = {"expense_categories": expense_categories, "income_categories": income_categories,
                   "transfer_categories": transfer_categories, "expense_form": expense_category_form,
                   "income_form": income_category_form}

        if request.method == 'POST':
            return create_category(request, context)

        return render(request, 'budgeteer/profile/categories.html', context=context)
    else:
        return redirect('budgeteer:home')


def delete_category(request, pk):
    category = TransactionCategory.objects.get(pk=pk)
    category.delete()

    messages.success(request, "Category Deleted")
    return redirect(f'/{request.user.username}/categories')


def archive_category(request, pk):
    category = TransactionCategory.objects.get(pk=pk)

    if category.archived:
        category.archived = False
        messages.success(request, "Category Archived")
    else:
        category.archived = True
        messages.success(request, "Category Unarchived")

    category.save()

    return redirect(f'/{request.user.username}/categories')


def delete_transaction(request, account_pk, transaction_pk):
    transaction_account = Account.objects.get(pk=account_pk)
    transaction = Transaction.objects.get(pk=transaction_pk)
    balance_adjustment = transaction.amount

    if transaction.transaction_type.type_name == "Income" or transaction.category.category[:4] == "From":
        balance_adjustment = -transaction.amount

    transaction_account.current_balance += balance_adjustment
    transaction_account.save()

    if transaction.transaction_type.type_name == "Transfer":
        delete_offset(request, transaction)

    transaction.delete()

    messages.success(request, "Transaction Deleted")
    return redirect(f'/{request.user.username}/{transaction_account.account_name}')


def graph_view(request):
    return graph(request)


def edit(request, username):
    if request.user.is_authenticated and request.user.username == username:
        return update_user(request)
    else:
        return redirect('budgeteer:home')


def budget(request, username):
    budget_objects = Budget.objects.filter(transaction_category__user=request.user).order_by('transaction_category')
    actual_amounts = dict()
    for budget in budget_objects:
        sum = Transaction.objects.filter(account__user=request.user,
                                         category__category=budget.transaction_category.category,
                                         date__month=5, date__year=2020).aggregate(Sum('amount'))

        actual_amounts[budget.transaction_category.category] = round(sum['amount__sum'], 2) if sum['amount__sum'] else 0

    context = {"budgets": budget_objects, "actuals": actual_amounts}

    if request.user.is_authenticated and request.user.username == username:
        return render(request, 'budgeteer/profile/budget/budget.html', context=context)
    else:
        return redirect('budgeteer:home')
