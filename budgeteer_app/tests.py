from django.test import TestCase
from budgeteer_app.models import User, TransactionType, AccountType, Account, Transaction, TransactionCategory
from decimal import Decimal
from datetime import date


# Create your tests here.
class FixturesTest(TestCase):
    fixtures = ['test_data.json']

    def test_fixture_data(self):
        account_type = AccountType.objects.get(pk=1)
        transaction_type = TransactionType.objects.get(pk=1)

        self.assertEqual(account_type.account_type, "Chequing")
        self.assertEqual(transaction_type.type_name, "Expense")


class UsernameDisplayNameTest(TestCase):
    def setUp(self):
        User.objects.create(username="TestUseR", password="123abc123")

    def test_display_and_username(self):
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.display_name, "TestUseR")


class AccountTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        account_type = AccountType.objects.get(pk=1)
        user = User.objects.create(username="TestUser", password="123abc123")
        Account.objects.create(account_name="Test", account_type=account_type, user=user, starting_balance=21.22)

    def test_account_type(self):
        account = Account.objects.get(pk=1)
        self.assertEqual(account.account_type.account_type, "Chequing")
        self.assertEqual(account.starting_balance, Decimal('21.22'))
        self.assertEqual(account.current_balance, account.starting_balance)


class ExpenseTransactionTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        account_type = AccountType.objects.get(pk=1)
        user = User.objects.create(username="TestUser", password="123abc123")
        account = Account.objects.create(account_name="Test", account_type=account_type, user=user,
                                         starting_balance=21.22)
        expense = TransactionType.objects.get(pk=1)

        category = TransactionCategory.objects.create(transaction_type=expense, category="Rent", user=user)

        Transaction.objects.create(account=account, date=date.today(), amount=12.32,
                                   transaction_type=expense, category=category, notes="This is a test")

    def test_expense(self):
        account = Account.objects.get(pk=1)
        self.assertEqual(account.starting_balance, Decimal('21.22'))
        self.assertEqual(account.current_balance, Decimal('8.90'))
