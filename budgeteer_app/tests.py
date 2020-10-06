from django.test import TestCase
from budgeteer_app.models import User, TransactionType, AccountType, Account, TransactionCategory, Transaction
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


class UserTest(TestCase):
    fixtures = ['test_data.json']

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

    def test_account_starting_balance(self):
        account = Account.objects.get(pk=1)
        self.assertEqual(account.starting_balance, Decimal('21.22'))

    def test_account_initial_current_balance(self):
        account = Account.objects.get(pk=1)
        self.assertEqual(account.current_balance, account.starting_balance)


class TransactionTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        chequing = AccountType.objects.get(pk=1)
        savings = AccountType.objects.get(pk=2)
        expense = TransactionType.objects.get(pk=1)
        income = TransactionType.objects.get(pk=2)
        user = User.objects.create(username="TestUser", password="123abc123")

        Account.objects.create(account_name="Test", account_type=chequing, user=user,
                               starting_balance=21.22)

        Account.objects.create(account_name="Test2", account_type=savings, user=user, starting_balance=100.00)

        TransactionCategory.objects.create(transaction_type=expense, category="Rent", user=user)
        TransactionCategory.objects.create(transaction_type=expense, category="Food", user=user)
        TransactionCategory.objects.create(transaction_type=income, category="Pay", user=user)

    def test_initial_archived_status(self):
        rent = TransactionCategory.objects.get(pk=1)
        self.assertFalse(rent.archived)

    def test_expense_transaction(self):
        account = Account.objects.get(pk=1)
        expense = TransactionType.objects.get(pk=1)
        food = TransactionCategory.objects.get(pk=2)
        transaction = Transaction.objects.create(account=account, date=date.today(), amount=Decimal('12.32'),
                                                 transaction_type=expense, category=food, notes="Test")

        self.assertEqual(account.current_balance, account.starting_balance - transaction.amount)
        self.assertEqual(account.current_balance, Decimal('8.90'))

    def test_income_transaction(self):
        account = Account.objects.get(pk=1)
        income = TransactionType.objects.get(pk=2)
        pay = TransactionCategory.objects.get(pk=3)
        transaction = Transaction.objects.create(account=account, date=date.today(), amount=Decimal('12.32'),
                                                 transaction_type=income, category=pay, notes="Test")

        self.assertEqual(account.current_balance, Decimal('33.54'))
        self.assertEqual(account.current_balance, account.starting_balance + transaction.amount)

    def test_transfer_from_transaction(self):
        chequing = Account.objects.get(pk=1)
        savings = Account.objects.get(pk=2)
        transfer = TransactionType.objects.get(pk=3)
        transfer_from = TransactionCategory.objects.get(category="From Test2")

        Transaction.objects.create(account=chequing, date=date.today(), amount=Decimal('50.00'),
                                   transaction_type=transfer, category=transfer_from, notes="Test")

        self.assertEqual(chequing.current_balance, chequing.starting_balance + 50)
        # Offsetting transaction happens in the view, so the From account will not have its balance updated
        self.assertEqual(savings.current_balance, savings.starting_balance)

    def test_transfer_to_transaction(self):
        chequing = Account.objects.get(pk=1)
        savings = Account.objects.get(pk=2)
        transfer = TransactionType.objects.get(pk=3)
        transfer_to = TransactionCategory.objects.get(category="To Test2")

        Transaction.objects.create(account=chequing, date=date.today(), amount=Decimal('1.22'),
                                   transaction_type=transfer, category=transfer_to, notes="Test")

        self.assertEqual(chequing.current_balance, chequing.starting_balance - Decimal('1.22'))
        # Offsetting transaction happens in the view, so the From account will not have its balance updated
        self.assertEqual(savings.current_balance, savings.starting_balance)

    def test_value_adjustment_increase_transaction(self):
        chequing = Account.objects.get(pk=1)
        value_adj = TransactionType.objects.get(pk=4)
        increase = TransactionCategory.objects.get(category="Increase")

        Transaction.objects.create(account=chequing, date=date.today(), amount=Decimal('8.78'),
                                   transaction_type=value_adj, category=increase)

        self.assertEqual(chequing.current_balance, Decimal('30.00'))

    def test_value_adjustment_decrease_transaction(self):
        chequing = Account.objects.get(pk=1)
        value_adj = TransactionType.objects.get(pk=4)
        decrease = TransactionCategory.objects.get(category="Decrease")

        Transaction.objects.create(account=chequing, date=date.today(), amount=Decimal('1.22'),
                                   transaction_type=value_adj, category=decrease)

        self.assertEqual(chequing.current_balance, Decimal('20.00'))
