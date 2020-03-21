from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


# Create your views here.
def home(request):
    return render(request , template_name="budgeteer/home.html")


def login(request):
    return HttpResponse("This is the login screen")


class AboutView(TemplateView):
    template_name = "about.html"
