from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate
from budgeteer_app.forms import CustomUserAuthForm


def validate_login(request, form):
    if form.is_valid():
        username = form.cleaned_data.get('username').lower()
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {user.display_name}")
            return redirect(f'/{user.username}')
        else:
            messages.error(request, "Invalid username or password")
            form = CustomUserAuthForm
            return render(request, "budgeteer/login.html", {"form": form})
    else:
        messages.error(request, "Invalid username or password")
        form = CustomUserAuthForm
        return render(request, "budgeteer/login.html", {"form": form})
