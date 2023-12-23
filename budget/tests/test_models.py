from datetime import date
import django.db.utils
from django.test import TestCase
from budget.models import Budget
from budget.tests.factories import BudgetFactory
from category.tests.factories import CategoryFactory
from transaction.tests.factories import TransactionFactory
from user_factory import UserFactory


class BudgetTestCase(TestCase):
    """
    Budget Test Case
    """

    def test_start_date_is_set_to_first_of_month(self):
        """
        Test start date is set to first of month
        """
        budget = BudgetFactory(start_date=date(2021, 1, 15))
        self.assertEqual(budget.start_date.day, 1)

    def test_budget_is_unique(self):
        """
        Test budget is unique
        """
        budget = BudgetFactory()
        with self.assertRaises(django.db.utils.IntegrityError):
            BudgetFactory(
                category=budget.category,
                start_date=budget.start_date,
            )


class BudgetSummaryTestCase(TestCase):
    """
    Budget Summary Test Case
    """

    def setUp(self):
        self.month = date(2021, 1, 1)
        self.user = UserFactory()
        self.category1 = CategoryFactory(user=self.user, income=False)
        self.category2 = CategoryFactory(user=self.user, income=False)
        self.income_category = CategoryFactory(user=self.user, income=True)

    def test_budget_summary(self):
        """
        Test budget summary
        """
        BudgetFactory(
            category=self.category1,
            start_date=self.month,
            user=self.user,
            amount=100,
        )
        BudgetFactory(
            category=self.category2,
            start_date=self.month,
            user=self.user,
            amount=200,
        )
        budget_summary = Budget.get_budget_by_category(self.month, self.user)
        self.assertEqual(len(budget_summary), 2)
        expected = [
            {
                "category": self.category1.category,
                "budget": 100,
                "actual": 0,
                "remaining": 100,
            },
            {
                "category": self.category2.category,
                "budget": 200,
                "actual": 0,
                "remaining": 200,
            },
        ]
        self.assertListEqual(budget_summary, expected)

    def test_budget_summary_does_not_include_income_categories(self):
        """
        Test budget summary does not include income categories
        """
        BudgetFactory(
            category=self.category1,
            start_date=self.month,
            user=self.user,
            amount=100,
        )
        BudgetFactory(
            category=self.income_category,
            start_date=self.month,
            user=self.user,
            amount=200,
        )
        budget_summary = Budget.get_budget_by_category(self.month, self.user)
        self.assertEqual(len(budget_summary), 1)

    def test_budget_summary_does_not_include_other_users_categories(self):
        """
        Test budget summary does not include other users categories
        """
        BudgetFactory(
            category=self.category1,
            start_date=self.month,
            user=self.user,
            amount=100,
        )
        BudgetFactory(
            category=self.category2,
            start_date=self.month,
            user=self.user,
            amount=200,
        )
        other_user = UserFactory()
        other_user_category = CategoryFactory(user=other_user)
        BudgetFactory(
            category=other_user_category,
            start_date=self.month,
            user=other_user,
            amount=200,
        )
        budget_summary = Budget.get_budget_by_category(self.month, self.user)
        self.assertEqual(len(budget_summary), 2)

    def test_budget_summary_uses_most_recent_budget_for_category(self):
        """
        Test budget summary uses most recent budget for category
        """
        BudgetFactory(
            category=self.category1,
            start_date=self.month,
            user=self.user,
            amount=100,
        )
        BudgetFactory(
            category=self.category1,
            start_date=self.month.replace(year=2020),
            user=self.user,
            amount=200,
        )
        budget_summary = Budget.get_budget_by_category(self.month, self.user)
        self.assertEqual(len(budget_summary), 1)
        expected = [
            {
                "category": self.category1.category,
                "budget": 100,
                "actual": 0,
                "remaining": 100,
            },
        ]
        self.assertListEqual(budget_summary, expected)

    def test_budget_summary_shows_budget_0_if_transaction_exists_but_no_budget(self):
        """
        Test budget summary shows budget 0 if transaction exists but no budget
        """
        TransactionFactory(
            category=self.category1,
            date=self.month,
            user=self.user,
            amount=100,
        )
        budget_summary = Budget.get_budget_by_category(self.month, self.user)
        self.assertEqual(len(budget_summary), 1)
        expected = [
            {
                "category": self.category1.category,
                "budget": 0,
                "actual": 100,
                "remaining": -100,
            },
        ]
        self.assertListEqual(budget_summary, expected)
