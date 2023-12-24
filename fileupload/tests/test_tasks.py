from django.test import TestCase
from category.tests.factories import CategoryFactory
from category.models import Category
from users.user_factory import UserFactory
from fileupload.tasks import sanitize_df
import pandas as pd


class SanitizeDFTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        # CategoryFactory.create_batch(10, user=self.user, income=False)
        # CategoryFactory.create_batch(2, user=self.user, income=True)
        self.categories = Category.objects.filter(user=self.user)
        self.df = pd.DataFrame(
            {
                "date": ["2020-01-01", "2020-01-02", "2020-01-03"],
                "description": ["test", "test", "test"],
                "code": ["test", "test", "test"],
                "income": ["", "", 10],
                "expense": [20, 20, ""],
                "category": ["", "", ""],
            }
        )

    def test_sanitize_df(self):
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertEqual(error_msg, "")
        self.assertEqual(df["income"].sum(), 10)
        self.assertEqual(df["expense"].sum(), 40)

    def test_sanitize_df_invalid_category(self):
        self.df["category"] = ["invalid", "invalid", "invalid"]
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn("Invalid", error_msg)

    def test_income_category_on_expense_row(self):
        income_category = self.categories.filter(income=True).first()
        self.df["category"][0] = income_category.category
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn(income_category.category, error_msg)

    def test_expense_category_on_income_row(self):
        expense_category = self.categories.filter(income=False).first()
        self.df["category"][2] = expense_category.category
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn(expense_category.category, error_msg)

    def test_future_date(self):
        self.df["date"][0] = "2051-01-01" # NOTE: FIXME in 30 years :)
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn("future", error_msg)

    def test_invalid_date(self):
        self.df["date"][0] = "invalid"
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn("Invalid date", error_msg)

    def test_both_income_and_expense(self):
        self.df["income"][0] = 10
        self.df["expense"][0] = 10
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn("both income and expense", error_msg)