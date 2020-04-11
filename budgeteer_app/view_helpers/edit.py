from django.shortcuts import redirect, render
from django.contrib import messages
from .general import form_errors
from budgeteer_app.forms import EditUser
from budgeteer_app.models import User


def update_user(request):
    form = EditUser (initial={"username": request.user.username , "display_name": request.user.display_name})

    if request.method == 'POST':
        form = EditUser(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            display_name = form.cleaned_data['display_name']

            if username != request.user.username and username not in [user.username for user in User.objects.all()]:
                messages.success(request, "Username Updated")
                request.user.username = username

            if display_name != request.user.display_name:
                messages.success(request, "Display Name Updated")
                request.user.display_name = display_name

            request.user.save()

            return redirect(f'/{request.user.username}')

        else:
            form_errors(request, form)
            return render(request, 'budgeteer/profile/edit.html', {"form": form})

    else:
        return render(request, 'budgeteer/profile/edit.html', {"form": form})