from budgeteer_app.models import TransactionCategory, TransactionType, Account, Transaction


# Returns the account name that a transfer was made based on the given category
def transfer_account(request, category):
    if category[:2] == "To":
        account_name = category[3:]
    else:
        account_name = category[5:]

    return Account.objects.get(user=request.user, account_name=account_name)


def transfer_category(request, account_name, category):
    if category[:2] == "To":
        category_name = "From " + account_name
    else:
        category_name = "To " + account_name

    transaction_type = TransactionType.objects.get(type_name="Transfer")

    return TransactionCategory.objects.get(user=request.user,
                                           category=category_name,
                                           transaction_type=transaction_type,
                                           )


def delete_offset(request, transaction):
    transfer_acct = transfer_account(request, transaction.category.category)
    transfer_cat = transfer_category(request, transaction.account.account_name, transaction.category.category)
    transaction_type = TransactionType.objects.get(type_name="Transfer")

    offsetting_transaction = Transaction.objects.get(date=transaction.date,
                                                     transaction_type=transaction_type,
                                                     account=transfer_acct,
                                                     amount=transaction.amount,
                                                     category=transfer_cat)

    if offsetting_transaction.category.category[:4] == "From":
        amount = transaction.amount * -1
        transfer_acct.current_balance += amount
    else:
        transfer_acct.current_balance += transaction.amount

    transfer_acct.save()
    offsetting_transaction.delete()
