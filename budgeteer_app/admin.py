from django.contrib import admin
#from django.contrib.auth.models import User
from .models import Account, AccountType

# Register your models here.
#admin.site.register(User)
admin.site.register(Account)
admin.site.register(AccountType)
