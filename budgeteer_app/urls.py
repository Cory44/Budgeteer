from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'budgeteer'

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('<username>', views.profile, name="profile"),
    # path ('about/', views.AboutView.as_view()),
]
