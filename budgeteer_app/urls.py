from django.urls import path
from django.contrib import admin
# from django.views.generic import TemplateView
from . import views

app_name = 'budgeteer'

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('graph_view/', views.graph_view, name="graph_view"),
    path('category/delete/<pk>', views.delete_category, name="delete_category"),
    path('category/archive/<pk>', views.archive_category, name="archive_category"),
    path('transaction/<account_pk>/<transaction_pk>', views.delete_transaction, name="delete_transaction"),
    path('<username>/', views.profile, name="profile"),
    path('<username>/edit', views.edit, name="edit"),
    path('<username>/add_account', views.add_account, name="add_account"),
    path('<username>/categories', views.categories, name="categories"),
    path('<username>/budget/<year>/<month>', views.budget, name="budget"),
    path('<username>/<account_name>', views.account, name="account"),
    path('<username>/<account_name>/add_transaction', views.add_transaction, name="add_transaction"),
]
