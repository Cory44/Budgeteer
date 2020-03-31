from budgeteer_app.models import Account, Transaction
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
from django.shortcuts import HttpResponse
import io


def graph(request):
    accounts = Account.objects.filter(user=request.user)

    today = datetime.date.today()
    starting_date = today
    starting_balance = 0

    for account in accounts:
        transactions = Transaction.objects.filter(account=account)

        starting_balance += account.starting_balance

        if len(transactions) > 0:
            transaction = transactions[len(transactions)-1]

            if transaction.date < starting_date:
                starting_date = transaction.date

    days = (today - starting_date).days

    dates = [starting_date + datetime.timedelta(days=i) for i in range(days)]

    daily_networth = {}

    daily_transaction_total = 0

    for day in dates:

        transactions = Transaction.objects.filter(account__user=request.user, date=day)

        for transaction in transactions:
            if transaction.transaction_type.type_name == "Expense":
                daily_transaction_total -= transaction.amount

            elif transaction.transaction_type.type_name == "Income":
                daily_transaction_total += transaction.amount

        daily_networth[day] = starting_balance + daily_transaction_total

    fig = Figure()
    canvas = FigureCanvas(fig)
    buf = io.BytesIO ()

    plt.plot(list(daily_networth.keys()), list(daily_networth.values()))
    plt.savefig(buf, format='png')
    plt.close(fig)

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    return response
