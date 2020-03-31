from budgeteer_app.models import Account, TransactionCategory, Transaction
from django.shortcuts import redirect


# Helps create an offsetting transaction for transfer transactions between a users accounts
def transfer(request, transaction):
    to_account_name = transaction.category.category.split(" ")[1]
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

    for transaction in transactions:  # Add transaction to
        transaction.account = Account.objects.get(account_name=account_name)

        if transaction.transaction_type.type_name == "Transfer":
            transfer(request, transaction)

        transaction.save()

    return redirect('budgeteer:home')
