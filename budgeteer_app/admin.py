from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account, AccountType, Transaction, TransactionType, TransactionCategory

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(Transaction)
admin.site.register(TransactionType)
admin.site.register(TransactionCategory)
