from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User class inheriting Djangos AbstractUser class. The username attribute is the unique identifier that a user
# uses to log into Budgeteer, it is stored in lowercase letters. The display_name attribute on the other hand, is a
# non-unique name that the user can set and change as needed, is for display purposes only. No email attribute is needed
# right now as it is not my intention to gather personal data for this project.
class User(AbstractUser):
    display_name = models.CharField(max_length=50, default=1, blank=False, null=False)

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):

        new_user = not self.pk

        if not self.pk:
            self.display_name = self.username
            self.username = self.username.lower()

        super(self.__class__, self).save(*args, **kwargs)

        if new_user:
            expense = TransactionType.objects.get(type_name='Expense')
            income = TransactionType.objects.get(type_name='Income')
            value_adj = TransactionType.objects.get(type_name='Value Adjustment')

            TransactionCategory.objects.create(user=self, transaction_type=expense, category="Groceries")
            TransactionCategory.objects.create(user=self, transaction_type=expense, category="Rent/Mortgage")
            TransactionCategory.objects.create(user=self, transaction_type=expense, category="Food & Drink")
            TransactionCategory.objects.create(user=self, transaction_type=expense, category="Personal Products")
            TransactionCategory.objects.create(user=self, transaction_type=expense, category="House Bills")
            TransactionCategory.objects.create(user=self, transaction_type=expense, category="Gifts")
            TransactionCategory.objects.create(user=self, transaction_type=income, category="Pay")
            TransactionCategory.objects.create(user=self, transaction_type=value_adj, category="Increase")
            TransactionCategory.objects.create(user=self, transaction_type=value_adj, category="Decrease")




# AccountType class only includes one field. The account_type objects include types like chequing, savings, credit card,
# investment, TFSA, RRSP, etc. These account types will be a global list of types, set by an administrator (i.e. a user
# will not be able to set their own account types)
class AccountType(models.Model):
    account_type = models.CharField(max_length=100)

    def __str__(self):
        return str(self.account_type)


# Account specific to a User, and has an AccountType. The current_balance is set to the starting_balance on creation.
# current_balance will only update when a user submits a transaction to that account.
class Account(models.Model):
    account_name = models.CharField(max_length=100)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_balance = models.DecimalField(max_digits=12, decimal_places=2)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.account_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        created = not self.pk

        if created:
            self.current_balance = self.starting_balance

        super().save()

        if created:
            transaction_type = TransactionType.objects.get(type_name="Transfer")
            TransactionCategory.objects.create(category="From " + self.account_name,
                                               transaction_type=transaction_type,
                                               user=self.user,
                                               account=self)

            TransactionCategory.objects.create(category="To " + self.account_name,
                                               transaction_type=transaction_type,
                                               user=self.user,
                                               account=self)

    def transaction(self, amount):
        self.current_balance += amount
        self.save()


# TransactionType only includes one field. The transaction_type objects includes three types; Expense, Income and
# Transfer. The types will be global, set by an administrator (i.e. a user will not be able to set their own account
# types)
class TransactionType(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.type_name)


# TransactionCategory is refined subtype of TransactionType, for example a transaction can have a TransactionType of
# Expense and a TransactionCategory of Groceries. Although an initial set of categories will be prepopulated, Users can
# edit and set their own TransactionCategories.
class TransactionCategory(models.Model):
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, blank=False, null=False)
    category = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    archived = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        if (self.transaction_type.type_name == "Expense" or self.transaction_type.type_name == "Income"):
            super (self.__class__ , self).save (*args , **kwargs)
            Budget.objects.create(transaction_category=self)


# Transaction is tied to an Account and a User through Account. Transaction has both, a TransactionType and a
# TransationCategory based on the TransactionType. Every time a Transaction is created or deleted, the current_balance
# attribute of the given account will be updated
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    notes = models.CharField(max_length=250)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.date) + " | " + str(self.amount) + ": " + self.notes

    def save(self, *args, **kwargs):
        amount = self.amount

        expense = self.transaction_type.type_name == "Expense"
        transfer_to = self.transaction_type.type_name == "Transfer" and self.category.category[:2] == "To"
        value_decrease = self.transaction_type.type_name == "Value Adjustment" and self.category.category == "Decrease"

        if expense or transfer_to or value_decrease:
            amount = -amount

        self.account.transaction(amount)
        super().save(*args, **kwargs)


class Budget(models.Model):
    PERIOD = (
        ('daily' , 'Daily') ,
        ('weekly' , 'Weekly') ,
        ('bi-weekly' , 'Bi-Weekly') ,
        ('semi-monthly' , 'Semi-monthly') ,
        ('monthly' , 'Monthly') ,
        ('quarterly' , 'Quarterly') ,
        ('semi-annually' , 'Semi-annually') ,
        ('annually' , 'Annually')
    )

    transaction_category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, blank=False, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    period = models.CharField(max_length=20, choices=PERIOD, default='monthly')