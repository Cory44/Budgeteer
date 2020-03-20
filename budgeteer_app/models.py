from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    display_name = models.CharField(max_length=50, default=1, blank=False, null=False)

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.display_name = self.username
            self.username = self.username.lower()
        super(self.__class__, self).save(*args, **kwargs)


class AccountType(models.Model):
    account_type = models.CharField(max_length=100)

    def __str__(self):
        return self.account_type


class Account(models.Model):
    account_name = models.CharField(max_length=100)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_balance = models.DecimalField(max_digits=12, decimal_places=2)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.account_name

    def transaction(self, amount):
        self.current_balance += amount
        self.save()


class TransactionType(models.Model):
    type_name = models.CharField(name="type", max_length=100)

    def __str__(self):
        return self.type_name


class TransactionCategory(models.Model):
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    notes = models.CharField(max_length=250)

    def __str__(self):
        return str(self.date) + " | " + str(self.amount) + ": " + self.notes

    def save(self, *args, **kwargs):
        amount = self.amount
        print(self.transaction_type == "Expense", amount, type(str(self.transaction_type)))

        if str(self.transaction_type) == "Expense" or (self.transaction_type == "Transfer"
                                                       and self.category[:2] == "To"):
            amount = -amount
            print("Here")

        print(amount)
        self.account.transaction(amount)

        super().save(*args, **kwargs)
