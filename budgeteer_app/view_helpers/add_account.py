from django.shortcuts import redirect, render
from django.contrib import messages
from .general import form_errors


def validate_account_form(request, form):
    if form.is_valid():
        display_account = form.save(commit=False)

        if len(request.user.account_set.filter(account_name=display_account.account_name)) > 0:
            messages.error(request, "Account name already taken")
            return render(request, 'budgeteer/profile/account/add_account.html', {"form": form})

        display_account.user = request.user
        form.save()

        messages.success(request, "Account added")
        return redirect('budgeteer:home')
    else:
        form_errors(request, form.errors)
        return render(request, 'budgeteer/profile/account/add_account.html', {"form": form})
