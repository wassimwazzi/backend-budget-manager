from django.test import TestCase
from users.user_factory import UserFactory
from .factories import TransactionFactory
from django.db.utils import IntegrityError


class TestTransaction(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_transaction_future_date(self):
        with self.assertRaises(IntegrityError):
            transaction = TransactionFactory(user=self.user, date="2050-01-01")

    def test_transaction_wrong_category(self):
        with self.assertRaises(IntegrityError):
            transaction = TransactionFactory(user=self.user)
            transaction.category.user = UserFactory()
            transaction.save()

    def test_transaction_null_code_and_description(self):
        with self.assertRaises(IntegrityError):
            transaction = TransactionFactory(
                user=self.user, code=None, description=None
            )
            transaction.save()

    def test_transaction_null_code(self):
        transaction = TransactionFactory(user=self.user, code=None)
        transaction.save()

    def test_transaction_null_description(self):
        transaction = TransactionFactory(user=self.user, description=None)
        transaction.save()

    def test_transaction_amount_zero(self):
        with self.assertRaises(IntegrityError):
            transaction = TransactionFactory(user=self.user, amount=0)
            transaction.save()

    def test_transaction_amount_negative(self):
        with self.assertRaises(IntegrityError):
            transaction = TransactionFactory(user=self.user, amount=-1)
            transaction.save()
