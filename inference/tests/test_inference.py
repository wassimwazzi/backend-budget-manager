from django.test import TestCase
from category.models import Category
from transaction.models import Transaction
from transaction.tests.factories import TransactionFactory
from users.user_factory import UserFactory
from ..inference import infer_categories


class YourTestCase(TestCase):
    def setUp(self):
        # Set up a user, categories, and transactions for testing
        self.user = UserFactory()
        self.income_category = Category.objects.filter(income=True).first()
        self.expense_category = Category.objects.filter(income=False).first()
        self.default_income_category = Category.objects.filter(
            income=True, is_default=True
        ).first()
        self.default_expense_category = Category.objects.filter(
            income=False, is_default=True
        ).first()

    def test_infer_categories_based_on_code(self):
        # Create a test transaction with a code for inference
        transaction = TransactionFactory(
            user=self.user, amount=200.0, code="A001", category=self.income_category
        )
        inferred_transaction = TransactionFactory(
            user=self.user,
            amount=100.0,
            code="A001",
            inferred_category=True,
            category=self.default_income_category,
        )
        transactions_to_infer = Transaction.objects.filter(id=inferred_transaction.id)
        # Call the infer_categories function
        infer_categories(transactions_to_infer, self.user)

        # Assert that the category is inferred based on code
        inferred_transaction.refresh_from_db()
        self.assertEqual(inferred_transaction.inferred_category, True)
        self.assertEqual(transaction.category, inferred_transaction.category)

    def test_infer_categories_based_on_description(self):
        # Create a test transaction with a description for inference
        transaction = TransactionFactory(
            user=self.user,
            amount=200.0,
            description="Income description",
            category=self.income_category,
        )
        inferred_transaction = TransactionFactory(
            user=self.user,
            amount=100.0,
            description="Income description",
            inferred_category=True,
            category=self.default_income_category,
        )
        transactions_to_infer = Transaction.objects.filter(id=inferred_transaction.id)
        # Call the infer_categories function
        infer_categories(transactions_to_infer, self.user)

        # Assert that the category is inferred based on description
        inferred_transaction.refresh_from_db()
        self.assertEqual(inferred_transaction.inferred_category, True)
        self.assertEqual(transaction.category, inferred_transaction.category)

    def test_does_not_use_income_category_on_expense_transactions(self):
        # Create a test transaction with a code for inference
        transaction = TransactionFactory(
            user=self.user, amount=200.0, code="A001", category=self.income_category
        )
        inferred_transaction = TransactionFactory(
            user=self.user,
            amount=100.0,
            code="A001",
            inferred_category=True,
            category=self.default_expense_category,
        )
        transactions_to_infer = Transaction.objects.filter(id=inferred_transaction.id)
        # Call the infer_categories function
        infer_categories(transactions_to_infer, self.user)

        # Assert that the category is inferred based on code
        inferred_transaction.refresh_from_db()
        self.assertEqual(inferred_transaction.inferred_category, True)
        self.assertNotEqual(transaction.category, inferred_transaction.category)
