from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AccountType(models.Model):
    account_type = models.CharField(max_length=100)

    def __str__(self):
        return self.account_type

class Account(models.Model):
    account_name = models.CharField(max_length=100)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.account_name
