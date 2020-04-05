from budgeteer_app.models import TransactionType
from budgeteer_app.forms import AddExpenseCategory
from django.contrib import messages
from django.shortcuts import render

def category_form_save(request, valid_form, type, context):
    category = valid_form.save(commit=False)
    category.transaction_type = TransactionType.objects.get(type_name=type)
    category.user = request.user
    category.save()

    messages.success(request, "Category Created")
    return render(request, 'budgeteer/profile/categories.html', context=context)


def create_category(request, context):
    if 'expense_category' in request.POST:
        expense_category_form_complete = AddExpenseCategory(request.POST, prefix="expense_category")

        if expense_category_form_complete.is_valid():
            return category_form_save(request, expense_category_form_complete, "Expense", context)
        else:
            return form_errors(request, expense.errors)

    elif 'income_category' in request.POST:
        income_category_form_complete = AddExpenseCategory(request.POST, prefix="income_category")

        if income_category_form_complete.is_valid():
            return category_form_save(request, income_category_form_complete, "Income", context)
        else:
            return form_errors(request, expense.errors)