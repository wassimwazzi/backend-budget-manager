from django.test import TestCase
from category.models import Category
from category.tests.factories import CategoryFactory
from transaction.models import Transaction
from users.user_factory import UserFactory
from .factories import FileUploadFactory
from ..models import Status
from fileupload.tasks import sanitize_df, create_transactions, process_file
import pandas as pd
import unittest.mock as mock

# silence this pandas warning: SettingWithCopyWarning
pd.options.mode.chained_assignment = None


class SanitizeDfTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        # CategoryFactory.create_batch(10, user=self.user, income=False)
        # CategoryFactory.create_batch(2, user=self.user, income=True)
        nan = float("nan")
        self.categories = Category.objects.filter(user=self.user)
        self.df = pd.DataFrame(
            {
                "date": ["2020-01-01", "2020-01-02", "2020-01-03"],
                "description": ["test", "test", "test"],
                "code": ["test", "test", "test"],
                "income": [nan, nan, 10],
                "expense": [20, 20, nan],
                "category": ["", "", ""],
            }
        )

    def test_sanitize_df(self):
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertEqual(error_msg, "")
        self.assertEqual(df["income"].sum(), 10)
        self.assertEqual(df["expense"].sum(), 40)

    def test_insensitive_on_column_names(self):
        self.df.columns = [
            "DATE",
            "DESCRIPTION",
            "CODE",
            "INCOME",
            "EXPENSE",
            "CATEGORY",
        ]
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertEqual(error_msg, "")
        self.assertEqual(df["income"].sum(), 10)
        self.assertEqual(df["expense"].sum(), 40)

    def test_missing_column(self):
        del self.df["date"]
        del self.df["income"]
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn("Missing", error_msg)
        self.assertIn("date", error_msg)
        self.assertIn("income", error_msg)

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
        self.df["date"][0] = "2051-01-01"  # NOTE: FIXME in 30 years :)
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

    def test_no_income_or_expense(self):
        self.df["income"][0] = float("nan")
        self.df["expense"][0] = float("nan")
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn("do not have income or expense", error_msg)

    def test_both_income_and_expense_are_zero(self):
        self.df["income"][0] = 0
        self.df["expense"][0] = 0
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn("do not have income or expense", error_msg)

    def test_negative_income(self):
        self.df["income"][0] = -10
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn("negative", error_msg)

    def test_negative_expense(self):
        self.df["expense"][0] = -10
        error_msg, df = sanitize_df(self.df, self.categories)
        self.assertIn("negative", error_msg)

    def test_category_case_insensitive(self):
        upper_case_category = CategoryFactory(
            user=self.user, category="TEST", income=False
        )
        df = pd.DataFrame(
            {
                "date": ["2020-01-01"],
                "description": ["test"],
                "code": ["test"],
                "income": [float("nan")],
                "expense": [20],
                "category": [upper_case_category.category.lower()],
            }
        )
        # self.df["category"][0] = self.categories.first().category.upper()
        categories = Category.objects.filter(user=self.user)
        error_msg, df = sanitize_df(df, categories)
        self.assertEqual(error_msg, "")


class TestCreateTranscations(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.categories = Category.objects.filter(user=self.user)
        self.file = FileUploadFactory(user=self.user)
        nan = float("nan")
        self.df = pd.DataFrame(
            {
                "date": ["2020-01-01", "2020-01-02", "2020-01-03"],
                "description": ["test", "test", "test"],
                "code": ["test", "test", "test"],
                "income": [nan, nan, 10],
                "expense": [20, 20, nan],
                "category": ["", "", ""],
            }
        )

    def test_create_transactions(self):
        error_msg = create_transactions(self.df, self.file, self.categories)
        self.assertEqual(error_msg, None)
        self.assertEqual(Transaction.objects.count(), 3)
        self.assertEqual(Transaction.objects.filter(category__income=True).count(), 1)
        self.assertEqual(Transaction.objects.filter(category__income=False).count(), 2)

    def test_create_transactions_invalid_date(self):
        self.df["date"][0] = "invalid"
        error_msg = create_transactions(self.df, self.file, self.categories)
        self.assertIn("invalid", error_msg)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_transactions_category_case_insensitive(self):
        upper_case_category = CategoryFactory(
            user=self.user, category="TEST", income=False
        )
        df = pd.DataFrame(
            {
                "date": ["2020-01-01"],
                "description": ["test"],
                "code": ["test"],
                "income": [float("nan")],
                "expense": [20],
                "category": [upper_case_category.category.lower()],
            }
        )
        error_msg = create_transactions(df, self.file, self.categories)
        self.assertEqual(error_msg, None)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.filter(category__income=False).count(), 1)


class TestProcessFile(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.categoties = Category.objects.filter(user=self.user)
        self.file = FileUploadFactory(user=self.user)
        self.file_contents = """date,description,code,income,expense,category
            2020-01-01,desc1,code1,,20,
            2020-01-02,desc2,code2,,20,
            2020-01-03,desc3,code3,10,,
        """

    def test_process_file(self):
        with mock.patch("builtins.open", mock.mock_open(read_data=self.file_contents)):
            res = process_file(self.file.id)(blocking=True)
            self.file.refresh_from_db()
        self.assertEqual(res, True)
        self.assertEqual(Transaction.objects.count(), 3)

    def test_when_amount_has_comma(self):
        self.file_contents = """date,description,code,income,expense,category
            2020-01-01,test,code1,,"1,000",
            2020-01-02,test,code2,,20.00,
            2020-01-03,test,code3,10.00,,
        """
        with mock.patch("builtins.open", mock.mock_open(read_data=self.file_contents)):
            res = process_file(self.file.id)(blocking=True)
            self.file.refresh_from_db()
        self.assertEqual(res, True)
        self.assertEqual(self.file.status, Status.COMPLETED)
        self.assertEqual(Transaction.objects.count(), 3)
        self.assertEqual(Transaction.objects.get(code="code1").amount, 1000)

    def test_adds_error_message_to_file_when_sanitize_df_fails(self):
        with mock.patch(
            "builtins.open", mock.mock_open(read_data=self.file_contents)
        ), mock.patch(
            "fileupload.tasks.sanitize_df", return_value=("Invalid date", None)
        ):
            res = process_file(self.file.id)(blocking=True)
            self.file.refresh_from_db()
        self.assertEqual(res, False)
        self.assertEqual(self.file.status, Status.FAILED)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertIn("Invalid date", self.file.message)

    def test_adds_error_message_to_file_when_create_transactions_fails(self):
        with mock.patch(
            "builtins.open", mock.mock_open(read_data=self.file_contents)
        ), mock.patch(
            "fileupload.tasks.create_transactions",
            return_value="Error creating transactions",
        ):
            res = process_file(self.file.id)(blocking=True)
            self.file.refresh_from_db()
        self.assertEqual(res, False)
        self.assertEqual(self.file.status, Status.FAILED)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertIn("Error creating transactions", self.file.message)

    def test_adds_generic_error_message_when_exception(self):
        with mock.patch(
            "builtins.open", mock.mock_open(read_data=self.file_contents)
        ), mock.patch(
            "fileupload.tasks.sanitize_df",
            side_effect=Exception("Something went wrong"),
        ), mock.patch(
            "logging.error", return_value=None
        ) as mock_logging:
            res = process_file(self.file.id)(blocking=True)
            self.file.refresh_from_db()
        self.assertEqual(res, False)
        self.assertEqual(self.file.status, Status.FAILED)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertIn("Error processing file", self.file.message)
        mock_logging.assert_called_once()
