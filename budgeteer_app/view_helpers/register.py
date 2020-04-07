from django.shortcuts import redirect, render
from django.contrib import messages
from .general import form_errors
from django.contrib.auth import login


def validate_registration(request, form):
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"New account created: {user.display_name}")
        return redirect(f'/{user.username}')
    else:
        form_errors(request, form.errors)
        return render(request, 'budgeteer/register.html', {"form": form})
