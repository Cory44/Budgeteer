from django.shortcuts import render, redirect
from .forms import CustomUserAuthForm, CustomUserCreationForm, AddAccountForm
from django.contrib.auth import logout as lout, login as lin, authenticate
from django.contrib import messages
from .models import Account


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
    if request.user.is_authenticated and request.user.username == username:
        return render(request, "budgeteer/profile/profile.html", {"username": username,
                                                                  "accounts": request.user.account_set.all()})
    else:
        return redirect('budgeteer:home')


def add_account(request, username):
    if request.user.is_authenticated and request.user.username == username:
        if request.method == "POST":
            form = AddAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                form.save()

                messages.success(request, "Account added")
                return render(request, "budgeteer/add_account.html", {"form": AddAccountForm()})
            else:
                for msg in form.errors:
                    for message in form.errors[msg]:
                        messages.error(request, f"{message}")

                return render(request, 'budgeteer/add_account.html', {"form": form})

        form = AddAccountForm()
        return render(request, "budgeteer/add_account.html", {"form": form})
    else:
        return redirect('budgeteer:home')
