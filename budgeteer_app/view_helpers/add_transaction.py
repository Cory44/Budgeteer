from budgeteer_app.models import Account, TransactionCategory, Transaction, TransactionType
from django.shortcuts import redirect


# Helps create an offsetting transaction for transfer transactions between a users accounts
def transfer(request, transaction):

    if transaction.category.category[:2] == "To":
        to_account_name = transaction.category.category[3:]
    else:
        to_account_name = transaction.category.category[5:]

    to_account = Account.objects.get(user=request.user, account_name=to_account_name)

    if transaction.category.category[:2] == "To":
        transfer_type = "From " + transaction.account.account_name
    else:
        transfer_type = "To " + transaction.account.account_name

    Transaction.objects.create(account=to_account, date=transaction.date, amount=transaction.amount,
                               transaction_type=transaction.transaction_type,
                               category=TransactionCategory.objects.get(user=request.user, category=transfer_type),
                               notes="Transfer")


def save_form(request, formset, account_name):
    transactions = formset.save(commit=False)
    account = Account.objects.get(account_name=account_name)
    formset.clean()

    for i in range(len(transactions)):  # Add transaction to
        transactions[i].account = account
        transactions[i].category =  formset[i].clean()['category']

        if transactions[i].transaction_type.type_name == "Transfer":
            transfer(request, transactions[i])

        transactions[i].save()

    return redirect('budgeteer:account', request.user.username, account)


def get_categories(request):
    expense = TransactionType.objects.get(type_name="Expense")
    income = TransactionType.objects.get(type_name="Income")
    transfer = TransactionType.objects.get(type_name="Transfer")
    # value_adjust = TransactionType.objects.get(type_name="Value Adjustment")

    expense_categories = TransactionCategory.objects.filter(user=request.user, transaction_type=expense)
    income_categories = TransactionCategory.objects.filter(user=request.user, transaction_type=income)
    transfer_categories = TransactionCategory.objects.filter(user=request.user, transaction_type=transfer)
    # value_adjust_categories = TransactionCategory.objects.filter(user=request.user, transaction_type=value_adjust)

    return expense_categories, income_categories, transfer_categories
            # "value_adjust": value_adjust_categories,


def custom_is_valid(formset):

    for error in formset.errors:
        for key in error:
            if key != 'category' and \
                    error[key][0] != 'Select a valid choice. That choice is not one of the available choices.':
                return False

    return True
