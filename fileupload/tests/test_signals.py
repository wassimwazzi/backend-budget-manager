from django.test import TestCase
from django.db.models import signals
from ..models import FileUpload, Status
from category.tests.factories import CategoryFactory
from transaction.models import Transaction
from user_factory import UserFactory
from .factories import FileUploadFactory
from ..signals import process_file
import unittest.mock
import pandas as pd


def mock_file_open(result_df, inferrence_mock=lambda df, categories: df):
    """
    decorator to call a function with the mock context manager
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            with unittest.mock.patch("builtins.open"), unittest.mock.patch(
                "pandas.read_csv"
            ) as mock_read_csv:
                mock_read_csv.return_value = result_df
                with unittest.mock.patch(
                    "inference.infer_categories"
                ) as mock_infer_categories:
                    mock_infer_categories.side_effect = inferrence_mock
                    return func(*args, **kwargs)

        return wrapper

    return decorator


class TestProcessFileSignal(TestCase):
    """
    Test process file signal
    """

    def setUp(self) -> None:
        def inferrence_mock(df, categories):
            df["Category"] = categories
            return df

        signals.post_save.disconnect(receiver=process_file, sender=FileUpload)
        self.user = UserFactory()
        self.category = CategoryFactory(user=self.user)
        self.df = pd.DataFrame(
            {
                "Date": ["2020-01-01", "2020-01-02", "2020-01-03"],
                "Description": ["Desc1", "Desc2", "Desc3"],
                "Amount": [10.0, 20.0, 30.0],
                "Category": [
                    self.category.category,
                    self.category.category,
                    self.category.category,
                ],
                "Code": ["Code1", "Code2", "Code3"],
            }
        )
        self.inferrence_mock = inferrence_mock
        self.file_upload = FileUploadFactory(user=self.user)

    def tearDown(self) -> None:
        # deletes the file in the upload_to directory
        self.file_upload.file.delete()

    def test_process_file(self):
        """
        Test process file
        """

        @mock_file_open(result_df=self.df)
        def test():
            process_file(sender=FileUpload, instance=self.file_upload, created=True)
            self.assertEqual(self.file_upload.status, Status.COMPLETED)
            self.assertEqual(self.file_upload.message, None)
            self.assertEqual(
                Transaction.objects.filter(file=self.file_upload).count(), 3
            )

        test()

    def test_process_file_missing_columns(self):
        """
        Test process file with missing columns
        """
        self.df.drop(columns=["Date", "Description", "Amount"], inplace=True)

        @mock_file_open(result_df=self.df)
        def test():
            process_file(sender=FileUpload, instance=self.file_upload, created=True)
            self.assertEqual(self.file_upload.status, Status.FAILED)
            self.assertIn("Missing columns", self.file_upload.message)
            self.assertIn("Date", self.file_upload.message)
            self.assertIn("Description", self.file_upload.message)
            self.assertIn("Amount", self.file_upload.message)
            self.assertEqual(
                Transaction.objects.filter(file=self.file_upload).count(), 0
            )

        test()

    def test_process_file_future_dates(self):
        """
        Test process file with future dates
        """
        self.df["Date"] = ["2030-01-01", "2020-01-02", "2020-01-03"]

        @mock_file_open(result_df=self.df)
        def test():
            process_file(sender=FileUpload, instance=self.file_upload, created=True)
            self.assertEqual(self.file_upload.status, Status.FAILED)
            self.assertEqual(
                self.file_upload.message, "rows [0] have dates in the future"
            )
            self.assertEqual(
                Transaction.objects.filter(file=self.file_upload).count(), 0
            )

        test()

    def test_process_file_missing_categories(self):
        """
        Test process file with missing categories
        """
        self.df["Category"] = ["Category1", "Category2", "Category3"]

        @mock_file_open(result_df=self.df)
        def test():
            process_file(sender=FileUpload, instance=self.file_upload, created=True)
            self.assertEqual(self.file_upload.status, Status.FAILED)
            self.assertIn("Missing categories", self.file_upload.message)
            self.assertIn("Category1", self.file_upload.message)
            self.assertIn("Category2", self.file_upload.message)
            self.assertIn("Category3", self.file_upload.message)
            self.assertEqual(
                Transaction.objects.filter(file=self.file_upload).count(), 0
            )

        test()

