from django.contrib import admin
#from django.contrib.auth.models import User
from .models import Account, AccountType, Transaction, TransactionType, TransactionCategory

# Register your models here.
#admin.site.register(User)
admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(Transaction)
admin.site.register(TransactionType)
admin.site.register(TransactionCategory)
